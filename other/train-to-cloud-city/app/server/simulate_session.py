# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import time
import train_types
from google.cloud import firestore
from fastapi.encoders import jsonable_encoder

PROJECT = "train-to-cloud-city-4"
COLLECTION = "global_simulation"
STEP_SEC = 5


logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')
log = logging.info

def sleep(duration):
    log(f"sleeping for {duration} seconds")
    time.sleep(duration)

def change(doc, data):
    log(f'{data}')
    doc.update(data)

# ----


train=train_types.Train(
        actual_location=train_types.LOCATION["STATION"],
        target_location=train_types.LOCATION["STATION"],
        actual_state="unknown",
    )
cargo = train_types.Cargo(actual_cargo=list())
signals={s.slug: s for s in train_types.SIGNALS}
pattern_slug="medium_complexity"
proposal=None
proposal_result=None


log("connecting to DB")
db = firestore.Client(project=PROJECT)
global_ref = db.collection(COLLECTION)

while True:
    log("set starting world state")
    
    cargo_doc = global_ref.document("cargo")
    cargo_doc.set(cargo.model_dump(mode="json"))

    train_doc = global_ref.document("train")
    train_doc.set(train.model_dump(mode="json"))

    signals_doc = global_ref.document("signals")
    signals_doc.set(jsonable_encoder(signals))

    proposal_doc = global_ref.document("proposal")
    proposal_doc.set({"pattern_slug":None, "proposal_result":None})
    # print(db.collection("global").document("proposal").get().to_dict()["pattern_slug"])


    sleep(STEP_SEC)    
    change(proposal_doc, {"pattern_slug":"pattern_d"})
    
    sleep(STEP_SEC)
    change(cargo_doc, {"actual_cargo" : ['cloud-storage']})

    sleep(STEP_SEC)
    change(cargo_doc, {"actual_cargo" : ['compute-engine', 'cloud-storage']})
    
    sleep(STEP_SEC)
    change(cargo_doc, {"actual_cargo" : ['compute-engine', 'cloud-storage', 'cloud-sql']})
    
    #exit()

    sleep(STEP_SEC)
    change(signals_doc, {"one.target_state" : "clear"})
    sleep(STEP_SEC / 2)
    change(signals_doc, {"one.actual_state" : "clear"})

    sleep(STEP_SEC)
    change(signals_doc, {"two.target_state" : "clear"})
    sleep(STEP_SEC / 2)
    change(signals_doc, {"two.actual_state" : "clear"})

    sleep(STEP_SEC)
    change(signals_doc, {"three.target_state" : "clear"})
    sleep(STEP_SEC / 2)
    change(signals_doc, {"three.actual_state" : "clear"})

    sleep(STEP_SEC)
    change(signals_doc, {"four.target_state" : "clear"})
    sleep(STEP_SEC / 2)
    change(signals_doc, {"four.actual_state" : "clear"})

    sleep(STEP_SEC)
    change(train_doc, {"target_location" : "one"})
    sleep(STEP_SEC)
    change(train_doc, {"target_location" : "two", "actual_location" : "one"})
    sleep(STEP_SEC)
    change(train_doc, {"target_location" : "three", "actual_location" : "two"})
    sleep(STEP_SEC)
    change(train_doc, {"target_location" : "four", "actual_location" : "three"})
    sleep(STEP_SEC)
    change(train_doc, {"target_location" : "station", "actual_location" : "four"})
    sleep(STEP_SEC)
    change(train_doc, {"actual_location" : "station"})

    sleep(20)

