# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#   kernelspec:
#     display_name: tech-coach-examples
#     language: python
#     name: tech-coach-examples
# ---

# %% [markdown]
# # Running multiple notebooks without papermill
#
# ## Code

# %%
import time

import child1
import child2


# %%
bucket = "gs://ssb-prod-dapla-felles-data-delt"
inndata_file = "tech-coach/automation/valuta_p2020_p2023-09-21_v1.parquet"
inndata_path = f"{bucket}/{inndata_file}"
print(f"{inndata_path=}")

process_step1_file = "tech-coach/automation/process_step1.parquet"
process_step1_path = f"{bucket}/{process_step1_file}"
print(f"{process_step1_path=}")

klargjort_file = "tech-coach/automation/valuta_monthly_p2022_v1.parquet"
klargjort_path = f"{bucket}/{klargjort_file}"
print(f"{klargjort_path=}")

# %%
start_time = time.time()
child1.run_all(inndata_path, process_step1_path)
child2.run_all(process_step1_path, klargjort_path)

# %%
execution_time = time.time() - start_time
print(f"Finished in {execution_time} seconds.")
