from llcsciencesdk.llc_api import ScienceSdk

llc_api = ScienceSdk(environment="production")
llc_api.login("username", "password")
sample = llc_api.update_map_layer_job_progress(
    map_layer_job_id=6,
    status="complete",
    step_id_to_update=1,
    started=False,
    percent_complete=90,
)
print(sample)
