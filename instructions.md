Here's the full schema reference for the Garmin Training API JSON format:

---

## Garmin Training API — Workout JSON Schema

---

### Top-Level Workout Object

```json
{
  "workoutId": 12345678,           // integer, assigned by Garmin on creation
  "workoutName": "5K Interval Run", // string, required
  "description": "...",            // string, optional
  "sportType": { ... },            // required — see Sport Types
  "estimatedDurationInSecs": 3600, // integer, optional
  "author": { ... },               // optional, set by Garmin
  "workoutSegments": [ ... ]       // array, required — the actual steps
}
```

---

### `sportType` Object

The sport type is declared both at the top level of the workout and repeated inside each segment.

```json
{
  "sportTypeId": 1,
  "sportTypeKey": "running"
}
```

| `sportTypeId` | `sportTypeKey` |
|---|---|
| 1 | `running` |
| 2 | `cycling` |
| 5 | `strength_training` |
| 17 | `indoor_cycling` |
| 3 | `other` |

---

### `workoutSegments` Array

Each segment groups a set of steps for one sport. Multi-sport workouts (e.g. triathlon) have multiple segments.

```json
{
  "segmentOrder": 1,         // integer, 1-based
  "sportType": { ... },      // same shape as top-level sportType
  "workoutSteps": [ ... ]    // array of step objects
}
```

---

### `workoutSteps` — Two Step Types

#### 1. `ExecutableStepDTO` — a single step

```json
{
  "type": "ExecutableStepDTO",
  "stepOrder": 1,              // integer, 1-based, unique across all steps
  "description": "Easy jog",  // optional
  "stepType": { ... },         // warmup / interval / rest / cooldown
  "endCondition": { ... },     // when the step ends
  "endConditionValue": 600,    // number — seconds, meters, or reps
  "targetType": { ... },       // optional — HR, pace, power, cadence
  "targetValueOne": 143,       // lower bound of target range
  "targetValueTwo": 157        // upper bound of target range
}
```

#### 2. `RepeatGroupDTO` — a loop of steps (for intervals/sets)

```json
{
  "type": "RepeatGroupDTO",
  "stepOrder": 1,
  "stepType": {
    "stepTypeId": 6,
    "stepTypeKey": "repeat"
  },
  "numberOfIterations": 4,           // how many times to repeat
  "endCondition": {
    "conditionTypeId": 7,
    "conditionTypeKey": "iterations"
  },
  "endConditionValue": 4.0,
  "skipLastRestStep": true,          // skip rest after final iteration
  "workoutSteps": [ ... ]            // nested ExecutableStepDTOs
}
```

---

### `stepType` Values

| `stepTypeId` | `stepTypeKey` | Usage |
|---|---|---|
| 1 | `warmup` | Opening warm-up |
| 2 | `cooldown` | Closing cool-down |
| 3 | `interval` | Main work step |
| 4 | `recovery` | Active recovery (shows `--` in app) |
| 5 | `rest` | Full rest between sets |
| 6 | `repeat` | Used only on `RepeatGroupDTO` |
| 7 | `other` | Generic step |

---

### `endCondition` — When a Step Ends

| `conditionTypeId` | `conditionTypeKey` | `endConditionValue` unit |
|---|---|---|
| 1 | `lap.button` | — (press lap to end) |
| 2 | `time` | seconds |
| 3 | `distance` | meters |
| 7 | `iterations` | count (for RepeatGroup) |
| 10 | `reps` | count (for strength steps) |
| 11 | `calories` | kcal |

> **Critical:** Garmin treats the numeric `conditionTypeId` as the source of truth. If the key and ID conflict, Garmin stores the condition that matches the ID.

---

### `targetType` — Intensity Target

The `targetValueOne` and `targetValueTwo` fields belong on the workout step alongside `targetType`, not nested inside it.

| `workoutTargetTypeId` | `workoutTargetTypeKey` | `targetValueOne/Two` |
|---|---|---|
| 1 | `no.target` | — |
| 2 | `power.zone` | zone number (1–7) |
| 3 | `cadence` | rpm |
| 4 | `heart.rate.zone` | bpm (custom range) |
| 5 | `speed` | m/s |
| 6 | `pace.zone` | m/s |
| 7 | `heart.rate` | zone number (1–5) |
| 8 | `power` | watts |
| 9 | `open` | — |

**Heart rate zone example (custom bpm range):**
```json
{
  "targetType": { "workoutTargetTypeId": 4, "workoutTargetTypeKey": "heart.rate.zone" },
  "targetValueOne": 143,
  "targetValueTwo": 157
}
```

**Pace zone example:**
Pace bounds use meters per second. For example, `targetValueOne: 1.9607843` and `targetValueTwo: 2.0833333` represents 8:00–8:30 min/km.
```json
{
  "targetType": { "workoutTargetTypeId": 6, "workoutTargetTypeKey": "pace.zone" },
  "targetValueOne": 1.9607843,
  "targetValueTwo": 2.0833333
}
```

---

### Strength-Specific Fields (on `ExecutableStepDTO`)

For strength workouts, each step uses `category` and `exerciseName` fields alongside a `weightUnit` object.

```json
{
  "type": "ExecutableStepDTO",
  "stepOrder": 2,
  "stepType": { "stepTypeId": 3, "stepTypeKey": "interval" },
  "endCondition": { "conditionTypeId": 10, "conditionTypeKey": "reps" },
  "endConditionValue": 10.0,
  "category": "SQUAT",
  "exerciseName": "GOBLET_SQUAT",
  "weightValue": 6.0,
  "weightUnit": {
    "unitId": 8,
    "unitKey": "kilogram",
    "factor": 1000.0
  }
}
```

| `weightUnit.unitKey` | `unitId` | `factor` |
|---|---|---|
| `kilogram` | 8 | 1000.0 |
| `pound` | 7 | 453.592 |

---

### Complete Running Workout Example

```json
{
  "workoutName": "Threshold Run",
  "sportType": { "sportTypeId": 1, "sportTypeKey": "running" },
  "estimatedDurationInSecs": 3600,
  "workoutSegments": [
    {
      "segmentOrder": 1,
      "sportType": { "sportTypeId": 1, "sportTypeKey": "running" },
      "workoutSteps": [
        {
          "type": "ExecutableStepDTO",
          "stepOrder": 1,
          "stepType": { "stepTypeId": 1, "stepTypeKey": "warmup" },
          "endCondition": { "conditionTypeId": 2, "conditionTypeKey": "time" },
          "endConditionValue": 600,
          "targetType": { "workoutTargetTypeId": 1, "workoutTargetTypeKey": "no.target" }
        },
        {
          "type": "RepeatGroupDTO",
          "stepOrder": 2,
          "stepType": { "stepTypeId": 6, "stepTypeKey": "repeat" },
          "numberOfIterations": 4,
          "endCondition": { "conditionTypeId": 7, "conditionTypeKey": "iterations" },
          "endConditionValue": 4.0,
          "skipLastRestStep": true,
          "workoutSteps": [
            {
              "type": "ExecutableStepDTO",
              "stepOrder": 3,
              "stepType": { "stepTypeId": 3, "stepTypeKey": "interval" },
              "endCondition": { "conditionTypeId": 3, "conditionTypeKey": "distance" },
              "endConditionValue": 1000,
              "targetType": { "workoutTargetTypeId": 6, "workoutTargetTypeKey": "pace.zone" },
              "targetValueOne": 2.5,
              "targetValueTwo": 2.778
            },
            {
              "type": "ExecutableStepDTO",
              "stepOrder": 4,
              "stepType": { "stepTypeId": 4, "stepTypeKey": "recovery" },
              "endCondition": { "conditionTypeId": 2, "conditionTypeKey": "time" },
              "endConditionValue": 90,
              "targetType": { "workoutTargetTypeId": 1, "workoutTargetTypeKey": "no.target" }
            }
          ]
        },
        {
          "type": "ExecutableStepDTO",
          "stepOrder": 5,
          "stepType": { "stepTypeId": 2, "stepTypeKey": "cooldown" },
          "endCondition": { "conditionTypeId": 2, "conditionTypeKey": "time" },
          "endConditionValue": 600,
          "targetType": { "workoutTargetTypeId": 1, "workoutTargetTypeKey": "no.target" }
        }
      ]
    }
  ]
}
```
---

## Garmin Training API — Swimming Workout Schema Extension

---

### Sport Type for Swimming

Swimming uses a different `sportTypeId` from running or cycling. There are two variants:

| `sportTypeId` | `sportTypeKey` | Use |
|---|---|---|
| 4 | `swimming` | all purpose |
| 26 | `pool_swimming` | Pool (structured, lap-counted) |
| 29 | `open_water_swimming` | Open water |

> **MUST DO ALWAYS** For **every** swimming workouts **must always use** `sportTypeId: 4` (`swimming`), as it would work on both sub types.

The `sportType` is declared both at the top level of the workout and repeated inside each `workoutSegment`. For swimming:

```json
{
  "workoutName": "Technique Set",
  "sportType": {
    "sportTypeId": 4,
    "sportTypeKey": "swimming"
  },
  "workoutSegments": [
    {
      "segmentOrder": 1,
      "sportType": {
        "sportTypeId": 4,
        "sportTypeKey": "swimming"
      },
      "poolLength": 25,
      "poolLengthUnit": {
        "unitId": 1,
        "unitKey": "meter",
        "factor": 1.0
      },
      "workoutSteps": [ ... ]
    }
  ]
}
```

---

### Pool Length — Segment-Level Field

`poolLength` is declared on the **segment**, not on individual steps. It tells the watch how long one lap is for distance tracking.

| `poolLengthUnit.unitKey` | `unitId` | Common lengths |
|---|---|---|
| `meter` | 1 | 25, 33.3, 50 |
| `yard` | 2 | 25, 33.3 |

```json
"poolLength": 50,
"poolLengthUnit": {
  "unitId": 1,
  "unitKey": "meter",
  "factor": 1.0
}
```

> **ALWAYS** set `poolLength` to 25 meters unless user indicates differently.

---

### Swimming `ExecutableStepDTO` — Additional Fields

A swimming step has the same base shape as other sports, but adds `swimStroke` and optionally `equipmentType` and `type` (drill descriptor).

```json
{
  "type": "ExecutableStepDTO",
  "stepOrder": 2,
  "description": "Freestyle pull set",
  "stepType": {
    "stepTypeId": 3,
    "stepTypeKey": "interval"
  },
  "endCondition": {
    "conditionTypeId": 3,
    "conditionTypeKey": "distance"
  },
  "endConditionValue": 200,

  "swimStroke": {
    "swimStrokeId": 1,
    "swimStrokeKey": "freestyle"
  },
  "equipmentType": {
    "equipmentTypeId": 3,
    "equipmentTypeKey": "pull_buoy"
  },
  "drillType": {
    "drillTypeId": 2,
    "drillTypeKey": "pull"
  }
}
```

---

### `swimStroke` Values

Stroke type identification is available only for pool swimming. Stroke types include freestyle, backstroke, and butterfly.

| `swimStrokeId` | `swimStrokeKey` | Notes |
|---|---|---|
| 0 | `any` | No specific stroke required |
| 1 | `freestyle` | Front crawl |
| 2 | `backstroke` | |
| 3 | `breaststroke` | |
| 4 | `butterfly` | Also called "fly" |
| 5 | `drill` | Generic drill (stroke unspecified) |
| 6 | `mixed` | Alternating strokes (e.g. IM) |

```json
"swimStroke": {
  "swimStrokeId": 3,
  "swimStrokeKey": "breaststroke"
}
```

---

### `equipmentType` Values

Supported equipment types for swimming steps are: `fins`, `kickboard`, `paddles`, and `pull_buoy`. Each step can carry **one** piece of equipment. If a step requires more than one item, you must remember to bring the additional equipment yourself — only one can be specified per step.

| `equipmentTypeId` | `equipmentTypeKey` | Purpose |
|---|---|---|
| 0 | `none` | No equipment |
| 1 | `fins` | Improve kick technique, build leg strength |
| 2 | `kickboard` | Isolate kick; legs only |
| 3 | `pull_buoy` | Isolate pull; arms only, legs float |
| 4 | `paddles` | Build arm strength and catch feel |
| 5 | `snorkel` | Focus on stroke without breathing disruption |

```json
"equipmentType": {
  "equipmentTypeId": 2,
  "equipmentTypeKey": "kickboard"
}
```

> **Tip:** Snorkel (`equipmentTypeId: 5`) may not be recognized by all Garmin devices. Verify against your target device model.

---

### `drillType` Values

Drill type refines what kind of movement the step focuses on, within a stroke:

| `drillTypeId` | `drillTypeKey` | Meaning |
|---|---|---|
| 0 | `none` | Full stroke |
| 1 | `kick` | Kick-only drill (e.g. with kickboard) |
| 2 | `pull` | Arms-only drill (e.g. with pull buoy) |
| 3 | `drill` | Other technique drill (catch-up, finger-tip drag, etc.) |

```json
"drillType": {
  "drillTypeId": 1,
  "drillTypeKey": "kick"
}
```

---

### `endCondition` for Swimming

Swimming steps are almost always distance-based, but time is valid too:

| Goal | `conditionTypeId` | `conditionTypeKey` | `endConditionValue` |
|---|---|---|---|
| Swim X meters | 3 | `distance` | meters (e.g. 100) |
| Rest for X seconds | 2 | `time` | seconds (e.g. 30) |
| Press lap to end | 1 | `lap.button` | — |
| Repeat N times | 7 | `iterations` | count (on RepeatGroupDTO) |

> Distance in swimming is **always in meters**, regardless of pool unit setting. Convert yards yourself if needed (1 yard = 0.9144 m).

---

### `stepType` — Swimming-Specific Conventions

The step types are shared with other sports, but swimming uses them with a specific convention:

| `stepTypeId` | `stepTypeKey` | Swimming convention |
|---|---|---|
| 1 | `warmup` | Opening easy swim, any stroke |
| 2 | `cooldown` | Closing easy swim |
| 3 | `interval` | Main work set (hard effort) |
| 4 | `recovery` | Active recovery between intervals |
| 5 | `rest` | Full stop rest (poolside) |
| 6 | `repeat` | Used only on `RepeatGroupDTO` |
| 7 | `other` | Drill sets, technique work |

---

### Complete Swimming Workout Example

A structured 2,400m session: warm-up → kick drill set → pull set → interval repeats → cool-down.

```json
{
  "workoutName": "Technique + Speed 2400m",
  "sportType": {
    "sportTypeId": 4,
    "sportTypeKey": "swimming"
  },
  "estimatedDurationInSecs": 3600,
  "workoutSegments": [
    {
      "segmentOrder": 1,
      "sportType": { "sportTypeId": 4, "sportTypeKey": "swimming" },
      "poolLength": 25,
      "poolLengthUnit": { "unitId": 1, "unitKey": "meter", "factor": 1.0 },
      "workoutSteps": [

        {
          "type": "ExecutableStepDTO",
          "stepOrder": 1,
          "description": "Easy warm-up, any stroke",
          "stepType": { "stepTypeId": 1, "stepTypeKey": "warmup" },
          "endCondition": { "conditionTypeId": 3, "conditionTypeKey": "distance" },
          "endConditionValue": 400,
          "swimStroke": { "swimStrokeId": 0, "swimStrokeKey": "any" },
          "equipmentType": { "equipmentTypeId": 0, "equipmentTypeKey": "none" }
        },

        {
          "type": "RepeatGroupDTO",
          "stepOrder": 2,
          "stepType": { "stepTypeId": 6, "stepTypeKey": "repeat" },
          "numberOfIterations": 4,
          "endCondition": { "conditionTypeId": 7, "conditionTypeKey": "iterations" },
          "endConditionValue": 4.0,
          "skipLastRestStep": true,
          "workoutSteps": [
            {
              "type": "ExecutableStepDTO",
              "stepOrder": 3,
              "description": "Kick drill with kickboard",
              "stepType": { "stepTypeId": 7, "stepTypeKey": "other" },
              "endCondition": { "conditionTypeId": 3, "conditionTypeKey": "distance" },
              "endConditionValue": 50,
              "swimStroke": { "swimStrokeId": 1, "swimStrokeKey": "freestyle" },
              "equipmentType": { "equipmentTypeId": 2, "equipmentTypeKey": "kickboard" },
              "drillType": { "drillTypeId": 1, "drillTypeKey": "kick" }
            },
            {
              "type": "ExecutableStepDTO",
              "stepOrder": 4,
              "description": "Rest",
              "stepType": { "stepTypeId": 5, "stepTypeKey": "rest" },
              "endCondition": { "conditionTypeId": 2, "conditionTypeKey": "time" },
              "endConditionValue": 20
            }
          ]
        },

        {
          "type": "ExecutableStepDTO",
          "stepOrder": 5,
          "description": "Pull set with pull buoy",
          "stepType": { "stepTypeId": 3, "stepTypeKey": "interval" },
          "endCondition": { "conditionTypeId": 3, "conditionTypeKey": "distance" },
          "endConditionValue": 400,
          "swimStroke": { "swimStrokeId": 1, "swimStrokeKey": "freestyle" },
          "equipmentType": { "equipmentTypeId": 3, "equipmentTypeKey": "pull_buoy" },
          "drillType": { "drillTypeId": 2, "drillTypeKey": "pull" }
        },

        {
          "type": "RepeatGroupDTO",
          "stepOrder": 6,
          "stepType": { "stepTypeId": 6, "stepTypeKey": "repeat" },
          "numberOfIterations": 8,
          "endCondition": { "conditionTypeId": 7, "conditionTypeKey": "iterations" },
          "endConditionValue": 8.0,
          "skipLastRestStep": true,
          "workoutSteps": [
            {
              "type": "ExecutableStepDTO",
              "stepOrder": 7,
              "description": "Sprint 100m freestyle",
              "stepType": { "stepTypeId": 3, "stepTypeKey": "interval" },
              "endCondition": { "conditionTypeId": 3, "conditionTypeKey": "distance" },
              "endConditionValue": 100,
              "swimStroke": { "swimStrokeId": 1, "swimStrokeKey": "freestyle" },
              "equipmentType": { "equipmentTypeId": 0, "equipmentTypeKey": "none" }
            },
            {
              "type": "ExecutableStepDTO",
              "stepOrder": 8,
              "description": "Rest 30s",
              "stepType": { "stepTypeId": 5, "stepTypeKey": "rest" },
              "endCondition": { "conditionTypeId": 2, "conditionTypeKey": "time" },
              "endConditionValue": 30
            }
          ]
        },

        {
          "type": "ExecutableStepDTO",
          "stepOrder": 9,
          "description": "Easy cool-down",
          "stepType": { "stepTypeId": 2, "stepTypeKey": "cooldown" },
          "endCondition": { "conditionTypeId": 3, "conditionTypeKey": "distance" },
          "endConditionValue": 200,
          "swimStroke": { "swimStrokeId": 0, "swimStrokeKey": "any" },
          "equipmentType": { "equipmentTypeId": 0, "equipmentTypeKey": "none" }
        }

      ]
    }
  ]
}
```

---

### Key Differences from Running/Cycling

| Aspect | Running / Cycling | Swimming |
|---|---|---|
| Extra segment field | — | `poolLength` + `poolLengthUnit` |
| Stroke | — | `swimStroke` object on each step |
| Equipment | — | `equipmentType` object (one per step) |
| Drill type | — | `drillType` object |
| Distance unit | meters (for running) | always meters |
| Targets | pace, HR, power, cadence | generally `no.target` (Garmin Connect's swim builder doesn't expose pace zones to devices the same way) |

> **On swim targets:** Garmin's pool swim workout format doesn't reliably support pace zone targets the way running does — the watch tracks SWOLF and stroke count instead. The recommended pattern for swim intensity is to use `no.target` (`workoutTargetTypeId: 1`) and rely on step description text to communicate the effort level (e.g. "at threshold pace").

---

## Garmin Training API — Cycling Workout Schema Extension

> As with the rest of this documentation, the cycling fields are reverse-engineered from the unofficial Garmin Connect API. Numeric IDs are authoritative; key strings are cosmetic. Always verify by exporting a known-good workout from Garmin Connect and inspecting the JSON.

---

### Sport Types for Cycling

The confirmed sport type IDs from community tooling are: `cycling` (2) for generic/outdoor road cycling, and `indoor_cycling` (17) for trainer/turbo sessions. Additional subtypes observed in the wild:

| `sportTypeId` | `sportTypeKey` | When to use |
|---|---|---|
| 2 | `cycling` | Generic outdoor / road cycling |
| 17 | `indoor_cycling` | Smart trainer, turbo, Zwift-style |
| 24 | `mountain_biking` | MTB (off-road) |
| 25 | `gravel_cycling` | Gravel / mixed surface |
| 169 | `virtual_ride` | Virtual platform rides (Zwift, Rouvy, etc.) |

> **MUST DO ALWAYS** For **every** cycling workouts **must always use** `sportTypeId: 2` (`cycling`), as it would work on both a head unit outdoors and an indoor trainer. Garmin Connect will still show it under both cycling workout lists.

---

### Top-Level Workout Object (Cycling)

The shape is identical to running, just with a different `sportType`:

```json
{
  "workoutName": "Sweet Spot 3x12",
  "description": "Three 12-minute sweet spot intervals",
  "sportType": {
    "sportTypeId": 17,
    "sportTypeKey": "indoor_cycling"
  },
  "estimatedDurationInSecs": 4500,
  "workoutSegments": [
    {
      "segmentOrder": 1,
      "sportType": {
        "sportTypeId": 17,
        "sportTypeKey": "indoor_cycling"
      },
      "workoutSteps": [ ... ]
    }
  ]
}
```

---

### Cycling Target Types

Cycling supports all the common target types, plus a few that are more meaningful than for running:

| `workoutTargetTypeId` | `workoutTargetTypeKey` | `targetValueOne/Two` units | Notes |
|---|---|---|---|
| 1 | `no.target` | — | Free ride / unstructured |
| 2 | `power.zone` | zone number (1–7) | Named Garmin power zone |
| 3 | `cadence` | rpm | Pedalling cadence range |
| 4 | `heart.rate.zone` | bpm or zone number | Named HR zone or custom bpm |
| 5 | `speed` | m/s | Less common, use power instead |
| 6 | `pace.zone` | m/s | Rarely used for cycling |
| 8 | `power` | watts | **Custom watt range** (most precise) |

#### Named Power Zone (1–7)

Power zone targets use `workoutTargetTypeId: 2` with `zoneNumber` (1–7) to reference the user's configured zones, which automatically scale with FTP updates.

```json
{
  "targetType": {
    "workoutTargetTypeId": 2,
    "workoutTargetTypeKey": "power.zone"
  },
  "zoneNumber": 4
}
```

Garmin's 7-zone power model (percentages of FTP):

| Zone | Name | % FTP | Character |
|---|---|---|---|
| 1 | Active Recovery | < 55% | Easy spin |
| 2 | Endurance | 56–75% | All-day pace |
| 3 | Tempo | 76–90% | Comfortably hard |
| 4 | Threshold | 91–105% | FTP / sweet spot |
| 5 | VO2 Max | 106–120% | Very hard, 3–8 min |
| 6 | Anaerobic | 121–150% | Short hard bursts |
| 7 | Neuromuscular | > 150% | Sprints, < 30 s |

#### Custom Watt Range (Absolute)

Use `workoutTargetTypeId: 8` for a specific watt range, e.g. a sweet spot block:

```json
{
  "targetType": {
    "workoutTargetTypeId": 8,
    "workoutTargetTypeKey": "power"
  },
  "targetValueOne": 250,
  "targetValueTwo": 280
}
```

> **Limitation:** Absolute watt targets don't adjust when the rider's FTP changes. For plans that scale automatically, prefer named power zones (`workoutTargetTypeId: 2`).

#### Cadence Range

```json
{
  "targetType": {
    "workoutTargetTypeId": 3,
    "workoutTargetTypeKey": "cadence"
  },
  "targetValueOne": 85,
  "targetValueTwo": 95
}
```

Cadence can be combined with a power target by putting cadence in the description text, since each step only holds one `targetType`. The common convention is to set the primary (power) as the target and include cadence guidance in the `description` field.

#### Heart Rate Zone (Named)

```json
{
  "targetType": {
    "workoutTargetTypeId": 4,
    "workoutTargetTypeKey": "heart.rate.zone"
  },
  "zoneNumber": 2
}
```

#### Custom Heart Rate Range (bpm)

```json
{
  "targetType": {
    "workoutTargetTypeId": 4,
    "workoutTargetTypeKey": "heart.rate.zone"
  },
  "targetValueOne": 130,
  "targetValueTwo": 150
}
```

---

### `endCondition` — Cycling-Specific Usage

All the standard conditions apply. Cycling most commonly uses time, but distance is fully valid outdoors:

| Condition | `conditionTypeId` | `conditionTypeKey` | `endConditionValue` |
|---|---|---|---|
| Time | 2 | `time` | seconds |
| Distance | 3 | `distance` | meters |
| Lap button | 1 | `lap.button` | — |
| Calories | 4 | `calories` | kcal |
| Power | 5 | `power` | watts (end when you exceed/drop below) |
| Iterations | 7 | `iterations` | count (RepeatGroupDTO only) |

> **Indoor vs outdoor:** For indoor/trainer sessions, always use `time`. For outdoor rides, `distance` is often more practical (e.g. "3km climb at threshold").

---

### `stepType` — Cycling Conventions

Same IDs as all other sports, but with some cycling-specific usage patterns:

| `stepTypeId` | `stepTypeKey` | Cycling usage |
|---|---|---|
| 1 | `warmup` | Easy spin, 10–20 min, no or Z2 target |
| 2 | `cooldown` | Easy spin down, flush legs |
| 3 | `interval` | Main effort (VO2, threshold, sprint) |
| 4 | `recovery` | Active recovery between intervals (low power, high cadence) |
| 5 | `rest` | Full stop or near-zero power (rare indoors) |
| 7 | `other` | Drills (e.g. one-legged pedalling, cadence drill) |

---

### Indoor vs Outdoor — Key Differences

| Aspect | Outdoor (`sportTypeId: 2`) | Indoor (`sportTypeId: 17`) |
|---|---|---|
| GPS | Yes | No (ERG mode or manual) |
| Distance tracking | GPS-based | Speed sensor / virtual |
| Best end condition | `distance` or `time` | `time` |
| Power source | Power meter | Smart trainer or power meter |
| ERG mode | N/A | Trainer auto-adjusts resistance to hit watt target |
| Preferred target | Power zone or watt range | Power zone or watt range |

---

### Outdoor Cycling — Distance-Based Steps

For outdoor workouts where you want to hit a landmark (e.g. a known climb):

```json
{
  "type": "ExecutableStepDTO",
  "stepOrder": 2,
  "description": "Climb at threshold power",
  "stepType": { "stepTypeId": 3, "stepTypeKey": "interval" },
  "endCondition": { "conditionTypeId": 3, "conditionTypeKey": "distance" },
  "endConditionValue": 5000,
  "targetType": { "workoutTargetTypeId": 2, "workoutTargetTypeKey": "power.zone" },
  "zoneNumber": 4
}
```

---

### Complete Indoor Cycling Workout Example

A classic sweet spot session: warm-up → 3×12 min sweet spot (Z4) with 5 min recovery → cool-down.

```json
{
  "workoutName": "Sweet Spot 3x12",
  "description": "Three 12-minute sweet spot blocks at 88-94% FTP",
  "sportType": { "sportTypeId": 17, "sportTypeKey": "indoor_cycling" },
  "estimatedDurationInSecs": 4500,
  "workoutSegments": [
    {
      "segmentOrder": 1,
      "sportType": { "sportTypeId": 17, "sportTypeKey": "indoor_cycling" },
      "workoutSteps": [

        {
          "type": "ExecutableStepDTO",
          "stepOrder": 1,
          "description": "Easy spin warm-up, 80-90rpm",
          "stepType": { "stepTypeId": 1, "stepTypeKey": "warmup" },
          "endCondition": { "conditionTypeId": 2, "conditionTypeKey": "time" },
          "endConditionValue": 600,
          "targetType": { "workoutTargetTypeId": 2, "workoutTargetTypeKey": "power.zone" },
          "zoneNumber": 2
        },

        {
          "type": "RepeatGroupDTO",
          "stepOrder": 2,
          "stepType": { "stepTypeId": 6, "stepTypeKey": "repeat" },
          "numberOfIterations": 3,
          "endCondition": { "conditionTypeId": 7, "conditionTypeKey": "iterations" },
          "endConditionValue": 3.0,
          "skipLastRestStep": false,
          "workoutSteps": [
            {
              "type": "ExecutableStepDTO",
              "stepOrder": 3,
              "description": "Sweet spot — 88-94% FTP, cadence 88-92rpm",
              "stepType": { "stepTypeId": 3, "stepTypeKey": "interval" },
              "endCondition": { "conditionTypeId": 2, "conditionTypeKey": "time" },
              "endConditionValue": 720,
              "targetType": { "workoutTargetTypeId": 8, "workoutTargetTypeKey": "power" },
              "targetValueOne": 250,
              "targetValueTwo": 285
            },
            {
              "type": "ExecutableStepDTO",
              "stepOrder": 4,
              "description": "Active recovery — easy spin, flush legs",
              "stepType": { "stepTypeId": 4, "stepTypeKey": "recovery" },
              "endCondition": { "conditionTypeId": 2, "conditionTypeKey": "time" },
              "endConditionValue": 300,
              "targetType": { "workoutTargetTypeId": 2, "workoutTargetTypeKey": "power.zone" },
              "zoneNumber": 1
            }
          ]
        },

        {
          "type": "ExecutableStepDTO",
          "stepOrder": 5,
          "description": "Easy cool-down spin",
          "stepType": { "stepTypeId": 2, "stepTypeKey": "cooldown" },
          "endCondition": { "conditionTypeId": 2, "conditionTypeKey": "time" },
          "endConditionValue": 600,
          "targetType": { "workoutTargetTypeId": 2, "workoutTargetTypeKey": "power.zone" },
          "zoneNumber": 1
        }

      ]
    }
  ]
}
```

---

### Complete Outdoor Cycling Workout Example

A VO2 max session for outdoor use: warm-up → 5×5 min VO2 efforts with 5 min recovery → cool-down.

```json
{
  "workoutName": "VO2max 5x5",
  "description": "Five 5-minute VO2 max intervals, outdoor road",
  "sportType": { "sportTypeId": 2, "sportTypeKey": "cycling" },
  "estimatedDurationInSecs": 5400,
  "workoutSegments": [
    {
      "segmentOrder": 1,
      "sportType": { "sportTypeId": 2, "sportTypeKey": "cycling" },
      "workoutSteps": [

        {
          "type": "ExecutableStepDTO",
          "stepOrder": 1,
          "description": "Easy warm-up, include a few short pickups",
          "stepType": { "stepTypeId": 1, "stepTypeKey": "warmup" },
          "endCondition": { "conditionTypeId": 2, "conditionTypeKey": "time" },
          "endConditionValue": 1200,
          "targetType": { "workoutTargetTypeId": 2, "workoutTargetTypeKey": "power.zone" },
          "zoneNumber": 2
        },

        {
          "type": "RepeatGroupDTO",
          "stepOrder": 2,
          "stepType": { "stepTypeId": 6, "stepTypeKey": "repeat" },
          "numberOfIterations": 5,
          "endCondition": { "conditionTypeId": 7, "conditionTypeKey": "iterations" },
          "endConditionValue": 5.0,
          "skipLastRestStep": true,
          "workoutSteps": [
            {
              "type": "ExecutableStepDTO",
              "stepOrder": 3,
              "description": "VO2 max effort — very hard but sustainable",
              "stepType": { "stepTypeId": 3, "stepTypeKey": "interval" },
              "endCondition": { "conditionTypeId": 2, "conditionTypeKey": "time" },
              "endConditionValue": 300,
              "targetType": { "workoutTargetTypeId": 2, "workoutTargetTypeKey": "power.zone" },
              "zoneNumber": 5
            },
            {
              "type": "ExecutableStepDTO",
              "stepOrder": 4,
              "description": "Easy recovery spin",
              "stepType": { "stepTypeId": 4, "stepTypeKey": "recovery" },
              "endCondition": { "conditionTypeId": 2, "conditionTypeKey": "time" },
              "endConditionValue": 300,
              "targetType": { "workoutTargetTypeId": 2, "workoutTargetTypeKey": "power.zone" },
              "zoneNumber": 1
            }
          ]
        },

        {
          "type": "ExecutableStepDTO",
          "stepOrder": 5,
          "description": "Easy cool-down",
          "stepType": { "stepTypeId": 2, "stepTypeKey": "cooldown" },
          "endCondition": { "conditionTypeId": 2, "conditionTypeKey": "time" },
          "endConditionValue": 900,
          "targetType": { "workoutTargetTypeId": 2, "workoutTargetTypeKey": "power.zone" },
          "zoneNumber": 1
        }

      ]
    }
  ]
}
```
---

### Key Differences from Running and Swimming

| Aspect | Running | Swimming | Cycling |
|---|---|---|---|
| Primary target | Pace zone | No target (distance-based) | **Power zone or watts** |
| End condition | Time or distance | Distance (meters) | Time (indoor) or distance (outdoor) |
| Extra step fields | — | `swimStroke`, `equipmentType`, `drillType` | — (no extra fields) |
| `sportTypeId` options | 1 (run), 9 (trail) | 26 (pool), 29 (open water) | 2 (road), 17 (indoor), 24 (MTB), 25 (gravel) |
| Zone model | HR zones (1–5) | N/A | **Power zones (1–7)** |
| `skipLastRestStep` | Optional | Common for drills | **Important** — set to `true` to avoid a rest after the final interval |
| Cadence target | Rarely used | N/A | Common secondary constraint (note in `description`) |

> **On `skipLastRestStep`:** For cycling intervals with a recovery step inside a `RepeatGroupDTO`, set `skipLastRestStep: true` when you want to transition directly from the last effort into the cool-down, rather than doing an extra recovery spin. Set it to `false` (or omit it) when even the final interval should be followed by full recovery before moving on.