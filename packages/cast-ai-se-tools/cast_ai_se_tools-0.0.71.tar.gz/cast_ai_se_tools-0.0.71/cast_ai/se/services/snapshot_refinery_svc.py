import logging
from typing import Dict, Any

from cast_ai.se.constants import (WORKLOAD_MAP, POD_SPEC_KEYWORDS, CLOUD_TAINTS, NON_RELEVANT_NAMESPACES,
                                  K8S_WORKLOAD_TYPES, WORKLOAD_TYPES)
from cast_ai.se.models.refined_snapshot import RefinedSnapshot
from cast_ai.se.models.refined_snapshot_analysis import RefinedSnapshotAnalysis
from cast_ai.se.services.snapshot_reporting_svc import SnapshotReporter


class SnapshotRefinery:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._refined_snapshot = RefinedSnapshot()
        self._rs_metadata = RefinedSnapshotAnalysis()
        self._reporter = SnapshotReporter(self._rs_metadata, self._refined_snapshot)
        self._logger.info("Initialized SnapshotRefinery")

    @property
    def reporter(self):
        return self._reporter

    def refine_snapshot(self, snapshot_data: Dict[str, Any]):
        self._logger.info("Starting snapshot refinement")
        self._refine_snapshot_workloads(snapshot_data)
        self._refine_snapshot_pdbs(snapshot_data)
        self._karpenter_check(snapshot_data)
        self._windows_check(snapshot_data)
        self._summarize_rs_object_types()
        self._logger.info("Completed snapshot refinement")

    def _windows_check(self, snapshot_data: Dict[str, Any]) -> None:
        self._logger.info("Checking for Windows nodes")
        for node in snapshot_data.get("nodeList", {}).get("items", []):
            labels = node.get("metadata", {}).get("labels", {})
            if labels.get("kubernetes.io/os") == "windows":
                self._refined_snapshot.windows_flag = True
                self._logger.info("Windows node found")
                break

    def _karpenter_check(self, snapshot_data: Dict[str, Any]) -> None:
        self._logger.info("Checking for Karpenter presence")
        self._refined_snapshot.karpenter_flag = \
            ("ec2NodeClassesList" in snapshot_data and bool(snapshot_data["ec2NodeClassesList"]["items"]))
        if self._refined_snapshot.karpenter_flag:
            self._logger.info("Karpenter is present")

    def _refine_snapshot_workloads(self, snapshot_data: Dict[str, Any]) -> None:
        self._logger.info("Refining snapshot workloads")
        for workload_key in K8S_WORKLOAD_TYPES:
            if snapshot_data[workload_key]["items"]:
                self._logger.info(f"Starting to analyze workloads ({workload_key})...")
                for workload in snapshot_data[workload_key]["items"]:
                    if workload["metadata"]["namespace"] in NON_RELEVANT_NAMESPACES:
                        self._logger.info(f"Skipping workload in non-relevant namespace: {workload['metadata']['namespace']}")
                        continue
                    if workload_key == "replicaSetList" and "ownerReferences" in workload["metadata"].keys():
                        self._logger.info(f"Skipping replica set with owner references: {workload['metadata']['name']}")
                        continue
                    self._refine_workload(workload, workload_key)

    def _summarize_rs_object_types(self) -> None:
        self._logger.info("Summarizing refined snapshot object types")
        try:
            for workload_type, workload_list in self._refined_snapshot.workloads.__dict__.items():
                if workload_type not in WORKLOAD_TYPES:
                    continue
                self._rs_metadata.total_counters["total_workloads"] += len(workload_list)
                for workload in workload_list:
                    if workload_type not in self._rs_metadata.workloads_observed.keys():
                        self._rs_metadata.workloads_observed[workload_type] = {}
                    self._count_workload(workload, workload_type)
            for pdb in self._refined_snapshot.pdbs:
                self._count_pdb(pdb)
            self._rs_metadata.total_counters["total_pdbs"] = len(self._refined_snapshot.pdbs)
            self._logger.info("Completed summarizing refined snapshot object types")
        except Exception as e:
            self._logger.error(f"Error summarizing refined snapshot. error=[{str(e)}")

    def _count_pdb(self, pdb):
        self._logger.info(f"Counting PDB: {pdb['name']} in namespace: {pdb['namespace']}")
        if pdb["namespace"] not in self._rs_metadata.pdbs_observed["namespaces"]:
            self._rs_metadata.pdbs_observed["namespaces"][pdb["namespace"]] = {}
        self._rs_metadata.pdbs_observed["namespaces"][pdb["namespace"]][pdb["name"]] = pdb["index"]

    def _count_workload(self, workload, workload_type):
        self._logger.info(f"Counting workload: {workload['name']} in namespace: {workload['namespace']} of type: {workload_type}")
        if workload["namespace"] not in self._rs_metadata.workloads_observed[workload_type].keys():
            self._rs_metadata[workload_type][workload["namespace"]] = {}
        self._rs_metadata[workload_type][workload["namespace"]][workload["name"]] = workload["index"]
        for refined_reason in workload["refined_reason"]:
            self._rs_metadata.total_counters[refined_reason] += 1

    def _get_taints_or_tolerations(self, item: Dict[str, Any], keyword: str):
        self._logger.info(f"Getting {keyword} for item: {item.get('metadata', {}).get('name', 'unknown')}")
        taints_or_tolerations_list = []
        for taint_or_toleration in item["spec"][keyword]:
            if "key" not in taint_or_toleration.keys() or taint_or_toleration["key"] not in CLOUD_TAINTS:
                taints_or_tolerations_list.append(taint_or_toleration)
            else:
                if "key" not in item.keys():
                    self._logger.info(f'Ignored {keyword} as no key found')
                else:
                    self._logger.info(f'Ignored {keyword} as no key part of known cloud taints')
        return taints_or_tolerations_list

    def _refine_workload(self, workload: Dict[str, Any], workload_key: str):
        self._logger.info(f"Starting to refine workload with key: {workload_key}")
        new_refined_workload = {
            "name": workload["metadata"]["name"],
            "namespace": workload["metadata"]["namespace"],
            "refined_reason": [],
            "index": 0
        }
        self._logger.debug(f"Initialized new_refined_workload: {new_refined_workload}")
        self._refine_podspec(new_refined_workload, workload)
        self._logger.debug(f"Refined podspec for workload: {new_refined_workload['name']}")
        if "requests" not in workload["spec"]["containers"]["resources"].keys():
            self._logger.info(f"Added 'no_requests' to refined_reason for workload: {new_refined_workload['name']}")
            new_refined_workload["refined_reason"].append("no_requests")
        if len(new_refined_workload["refined_reason"]):
            self._logger.info(f"Added refined workload to snapshot: {new_refined_workload['name']} with reasons: {new_refined_workload['refined_reason']}")
            self._refined_snapshot.workloads.add_item(WORKLOAD_MAP[workload_key], new_refined_workload)
        else:
            self._logger.info(f"No refinement reasons found for workload: {new_refined_workload['name']}")

    def _refine_podspec(self, new_refined_workload: Dict[str, Any], workload: Dict[str, Any]) -> None:
        self._logger.info(f"Refining podspec for workload: {new_refined_workload['name']}")
        for spec_keyword in POD_SPEC_KEYWORDS:
            if spec_keyword in workload["spec"]["template"]["spec"].keys():
                new_refined_workload[spec_keyword] = workload["spec"]["template"]["spec"][spec_keyword]
                self._logger.info(f"Added {spec_keyword} to {new_refined_workload['name']}")
                new_refined_workload["refined_reason"].append(spec_keyword)

    def _refine_snapshot_pdbs(self, snapshot_data: Dict[str, Any]) -> None:
        self._logger.info("Refining snapshot PDBs")
        if snapshot_data["podDisruptionBudgetList"]["items"]:
            for pdb in snapshot_data["podDisruptionBudgetList"]["items"]:
                if pdb["metadata"]["namespace"] in NON_RELEVANT_NAMESPACES:
                    self._logger.info(f"Skipping PDB in non-relevant namespace: {pdb['metadata']['namespace']}")
                    continue
                current_healthy = pdb.get('status', {}).get('currentHealthy')
                disruptions_allowed = pdb.get('status', {}).get('disruptionsAllowed')
                if current_healthy is not None and disruptions_allowed is not None:
                    if disruptions_allowed != 0:
                        self._logger.info(f"Skipping PDB with disruptions allowed: {pdb['metadata']['name']}")
                        continue

                self._logger.info(f'Found PDB {pdb["metadata"]["name"]} in {pdb["metadata"]["namespace"]}')
                self._refine_pdb(pdb)

    def _refine_pdb(self, pdb: Dict[str, Any]) -> None:
        self._logger.info(f"Refining PDB: {pdb['metadata']['name']} in namespace: {pdb['metadata']['namespace']}")
        new_refined_pdb = {"name": pdb["metadata"]["name"],
                           "namespace": pdb["metadata"]["namespace"],
                           "spec": pdb["spec"],
                           "index": len(self._refined_snapshot.pdbs),
                           "disruptions_allowed": pdb["status"]["disruptionsAllowed"],
                           "current_healthy": pdb["status"]["currentHealthy"]
                           }
        self._refined_snapshot.pdbs.append(new_refined_pdb)
        self._logger.info(f"Added refined PDB: {new_refined_pdb['name']} to snapshot")
