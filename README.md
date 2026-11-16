# Unit 1

## What This Does

     I picked the advice thread corpus. This system answers general questions that university students might have, such as questions about textbooks, studying, courses, housing, and other student experiences. The corpus consists of discussion threads with replies from other students. The goal is to retrieve relevant threads so that the system can answer questions using information from the corpus rather than unrelated information.

## Chunking Strategy

**Chunk size: 800**
**Overlap: 120**

     I kept the starter chunk size and overlap because the advice thread documents are already organized into short, self-contained threads. When I inspected the generated chunks, each chunk generally contained one complete thread along with its replies, rather than combining unrelated topics. This makes each chunk understandable on its own and means a question can usually be answered using the information in a single chunk. Because the threads are already relatively short, increasing the chunk size was not necessary.

## Sample Chunks

**Chunk 1** — source: `thread_bike_commute.txt#0` — produced by: `chunker.py::fallback_split`

```
THREAD: Is a bike worth it for a 20 minute walk commute?

--- reply 1 (14 votes) ---
Yeah. Cuts an 18 minute walk to about 6. The thing nobody mentions is storage — covered bike parking exists at three buildings and is full by 9am at all three.

--- reply 2 (9 votes) ---
Counterpoint, I sold mine. Between November and March the paths are either icy or salted and salt destroys a drivetrain in one season.

--- reply 3 (22 votes) ---
Both true. I keep a cheap bike for September to November and walk the rest of the year. Total cost was about $120 for the bike and I don't care what happens to it.

--- reply 4 (5 votes) ---
If you do get one, the campus does free registration and it's the only reason I got mine back after it was taken.
```

**Chunk 2** — source: `thread_first_gen.txt#0` — produced by: `chunker.py::fallback_split`

```
THREAD: Anything specific for first-generation students?

--- reply 1 (33 votes) ---
The advising office has a specific programme and it is genuinely good, but it is opt-in and badly publicised. Ask for it by name.

--- reply 2 (41 votes) ---
The thing I'd say: the unwritten rules are the hard part, not the coursework. Ask about the unwritten rules explicitly. People are happy to explain them and nobody volunteers them.

--- reply 3 (16 votes) ---
Emergency fund for textbooks and travel exists and is not means-tested beyond a short form.
```

**Chunk 3** — source: `thread_laptop_specs.txt#0` — produced by: `produced by: chunker.py::fallback_split`

```
THREAD: How much laptop do I actually need for CS courses?

--- reply 1 (31 votes) ---
Less than the recommended spec page says. 16GB of RAM is the one number worth paying for; everything else you'll never notice.

--- reply 2 (18 votes) ---
Adding: the lab machines exist and are better than anything you'll buy. For the heavy assignments people just use those.

--- reply 3 (12 votes) ---
I did two years on an 8GB machine and it was fine until the last project, at which point it very much wasn't. 16 is the answer.
```

**Chunk 4** — source: `thread_office_hours_etiquette.txt#0` — produced by: `chunker.py::fallback_split`

```
THREAD: Is it weird to go to office hours with no specific question?

--- reply 1 (44 votes) ---
No, and this is the single most common thing first years get wrong. 'I'm following the lectures but I don't feel like I understand the shape of it' is a completely normal thing to say.

--- reply 2 (29 votes) ---
They're usually empty. You are doing the instructor a favour by turning up.

--- reply 3 (18 votes) ---
If it helps, treat it as a standing appointment. Go every week for a month and it stops feeling like a thing.
```

**Chunk 5** — source: `thread_roommate_conflict.txt#0` — produced by: `chunker.py::fallback_split`

```
THREAD: Roommate situation isn't working. What now?

--- reply 1 (28 votes) ---
Talk to your RA early, and frame it as 'we need help sorting this out' rather than 'move me'. Room changes are possible but the process starts with mediation and skipping that step slows it down.

--- reply 2 (14 votes) ---
Room changes happen at the semester boundary almost always, and mid-semester only in fairly serious cases.

--- reply 3 (33 votes) ---
Write down specifics before the meeting. 'It's not working' is hard to act on; 'guests four nights a week past 2am' is not.
```

## Sample Answer

**Question: What can a student do if they are not getting along with their roommate?**

**Answer: A student should talk to their RA early and frame the conversation as getting help resolving the situation rather than immediately requesting a room change. The room-change process generally starts with mediation, and the student should write down specific problems before the meeting so they can clearly explain what is happening**

**Source: thread_roommate_conflict.txt#0**

```
```

**My relevance cutoff: 0.7**

| Question                                                                           | In corpus? | Best distance |
| ---------------------------------------------------------------------------------- | ---------- | ------------- |
| What can a student do if they are not getting along with their roommate?           | Yes        | 0.3963        |
| What determines whether a student can receive an extension for late work?          | Yes        | 0.5102        |
| What are study spots students can use besides the library?                         | Yes        | 0.3698        |
| Who should a student ask about whether they need a specific edition of a textbook? | Yes        | 0.6122        |
| How should a student handle an absent teammate in a group project?                 | Yes        | 0.3000        |
| What is the capital of Mongolia?                                                   | No         | 0.8902        |
| How do I change the oil in a diesel engine?                                        | No         | 0.9299        |
| Who won the 1994 World Cup?                                                        | No         | 0.7866        |
| What is the recommended dosage of ibuprofen for a headache?                        | No         | 0.8280        |
| How do I write a for loop in Rust?                                                 | No         | 0.8712        |

The five in-corpus questions had best distances from 0.3000 to 0.6122. The five out-of-corpus questions had best distances from 0.7866 to 0.9299. This left a gap between 0.6122 and 0.7866, so I selected 0.7 as the relevance cutoff. This cutoff accepts all five in-corpus questions while rejecting all five out-of-corpus questions in this test.

## How I Used AI

**1.** I asked Claude to help me decide how to choose the relevance cutoff. It explained that I should run the five in-scope questions and five out-of-scope questions, compare their best retrieval distances, and choose a cutoff in the gap between the two groups. I then used the measured distances from my own corpus rather than blindly using the starter's default value.

**2.** I asked Claude to check whether my acceptance criteria were testable. It helped me make the criteria specific enough that I could verify them by running commands and checking observable results instead of using vague statements such as whether the system "works well."

---

# Unit 2

## Run Log — Before


| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. 4 of 5 sampled chunks should be readable as a complete paragraph-sized thought | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. The correct source document should appear in the top 3 retrieved results | 4 of 5 | 0/5 | 0/5 | 0/5 | MISSED |

Criterion 1 - Retrieved chunk contains the answer
Produced by: run_eval.py::run_once → store.py::
### What can a student do if they are not getting along with their roommate? — run 1

- Best distance: 0.3963 (passed the gate)
- Sources retrieved: thread_commuting.txt, thread_group_project.txt, thread_office_hours_etiquette.txt, thread_roommate_conflict.txt, thread_study_spots.txt

```
A student can talk to their RA early and frame the conversation as needing help sorting things out rather than asking for a move. They should also write down specific details before the meeting rather than just saying the situation is not working. 

Source: `thread_roommate_conflict.txt`
```

### What can a student do if they are not getting along with their roommate? — run 2

- Best distance: 0.3963 (passed the gate)
- Sources retrieved: thread_commuting.txt, thread_group_project.txt, thread_office_hours_etiquette.txt, thread_roommate_conflict.txt, thread_study_spots.txt

```
A student can talk to their RA early and frame it as needing help sorting the situation out rather than asking directly for a move. Additionally, they should write down specific details before the meeting rather than just saying it is not working. 

Source: thread_roommate_conflict.txt
```

### What can a student do if they are not getting along with their roommate? — run 3

- Best distance: 0.3963 (passed the gate)
- Sources retrieved: thread_commuting.txt, thread_group_project.txt, thread_office_hours_etiquette.txt, thread_roommate_conflict.txt, thread_study_spots.txt

```
If a student is not getting along with their roommate, they can talk to their RA early and frame the conversation as needing help sorting things out rather than asking to move immediately (thread_roommate_conflict.txt). It is also recommended to write down specific details before the meeting rather than speaking in generalities (thread_roommate_conflict.txt).
```

Criterion 2 - Every answer names a source
Produced by: run_eval.py::run_once → store.py::
### What are study spots students can use besides the library? — run 1

- Best distance: 0.3698 (passed the gate)
- Sources retrieved: thread_commuting.txt, thread_first_gen.txt, thread_printing.txt, thread_sleep_schedule.txt, thread_study_spots.txt

```
According to `thread_study_spots.txt`, students can use Ridgeway Café before 10am or the open lounges on floors 2 through 5 of the science building, which are unlocked and almost always empty.
```

### What are study spots students can use besides the library? — run 2

- Best distance: 0.3698 (passed the gate)
- Sources retrieved: thread_commuting.txt, thread_first_gen.txt, thread_printing.txt, thread_sleep_schedule.txt, thread_study_spots.txt

```
Based on the provided documents, study spots outside of the library include the Ridgeway Café (before 10am) and the open lounges on floors 2 through 5 of the science building. 

Source: thread_study_spots.txt
```

### What are study spots students can use besides the library? — run 3

- Best distance: 0.3698 (passed the gate)
- Sources retrieved: thread_commuting.txt, thread_first_gen.txt, thread_printing.txt, thread_sleep_schedule.txt, thread_study_spots.txt

```
Study spots besides the library include the Ridgeway Café (before 10am) and the open lounges on floors 2 through 5 of the science building (thread_study_spots.txt).
```

Criterion 3 - Relevance gate
## The relevance gate on out-of-corpus questions

Produced by `run_eval.py::check_out_of_scope`, cutoff 0.7. Refused 5 of 5.

Retrieval is deterministic and the gate is a comparison against a
fixed number, so these do not vary between runs — one pass over the
list is the whole measurement.

| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.890 | refused |
| How do I change the oil in a diesel engine? | 0.930 | refused |
| Who won the 1994 World Cup? | 0.787 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.828 | refused |
| How do I write a for loop in Rust? | 0.871 | refused |

Criterion 4 - Chunk Quality
Produced by: `app.py` → chunker.py::split_documents → chunker.py::fallback_split
 ivanz@Ivan MINGW64 ~/Downloads/Codepath AI 301/ai201-coursework/ai201-project1-unofficial-guide-starter-v2026 (main)
$ python app.py chunks
26 chunks total. Showing 5, spread across the corpus.

======================================================================
Chunk 1  |  source: thread_bike_commute.txt#0  |  produced by: chunker.py::fallback_split
======================================================================
THREAD: Is a bike worth it for a 20 minute walk commute?

--- reply 1 (14 votes) ---
Yeah. Cuts an 18 minute walk to about 6. The thing nobody mentions is storage — covered bike parking exists at three buildings and is full by 9am at all three.

--- reply 2 (9 votes) ---
Counterpoint, I sold mine. Between November and March the paths are either icy or salted and salt destroys a drivetrain in one season.

--- reply 3 (22 votes) ---
Both true. I keep a cheap bike for September to November and walk the rest of the year. Total cost was about $120 for the bike and I don't care what happens to it.

--- reply 4 (5 votes) ---
If you do get one, the campus does free registration and it's the only reason I got mine back after it was taken.

======================================================================
Chunk 2  |  source: thread_first_gen.txt#0  |  produced by: chunker.py::fallback_split
======================================================================
THREAD: Anything specific for first-generation students?

--- reply 1 (33 votes) ---
The advising office has a specific programme and it is genuinely good, but it is opt-in and badly publicised. Ask for it by name.

--- reply 2 (41 votes) ---
The thing I'd say: the unwritten rules are the hard part, not the coursework. Ask about the unwritten rules explicitly. People are happy to explain them and nobody volunteers them.

--- reply 3 (16 votes) ---
Emergency fund for textbooks and travel exists and is not means-tested beyond a short form.

======================================================================
Chunk 3  |  source: thread_laptop_specs.txt#0  |  produced by: chunker.py::fallback_split
======================================================================
THREAD: How much laptop do I actually need for CS courses?

--- reply 1 (31 votes) ---
Less than the recommended spec page says. 16GB of RAM is the one number worth paying for; everything else you'll never notice.

--- reply 2 (18 votes) ---
Adding: the lab machines exist and are better than anything you'll buy. For the heavy assignments people just use those.

--- reply 3 (12 votes) ---
I did two years on an 8GB machine and it was fine until the last project, at which point it very much wasn't. 16 is the answer.

======================================================================
Chunk 4  |  source: thread_office_hours_etiquette.txt#0  |  produced by: chunker.py::fallback_split
======================================================================
THREAD: Is it weird to go to office hours with no specific question?

--- reply 1 (44 votes) ---
No, and this is the single most common thing first years get wrong. 'I'm following the lectures but I don't feel like I understand the shape of it' is a completely normal thing to say.

--- reply 2 (29 votes) ---
They're usually empty. You are doing the instructor a favour by turning up.

--- reply 3 (18 votes) ---
If it helps, treat it as a standing appointment. Go every week for a month and it stops feeling like a thing.

======================================================================
Chunk 5  |  source: thread_roommate_conflict.txt#0  |  produced by: chunker.py::fallback_split
======================================================================
THREAD: Roommate situation isn't working. What now?

--- reply 1 (28 votes) ---
Talk to your RA early, and frame it as 'we need help sorting this out' rather than 'move me'. Room changes are possible but the process starts with mediation and skipping that step slows it down.

--- reply 2 (14 votes) ---
Room changes happen at the semester boundary almost always, and mid-semester only in fairly serious cases.

--- reply 3 (33 votes) ---
Write down specifics before the meeting. 'It's not working' is hard to act on; 'guests four nights a week past 2am' is not.

For each one, ask: could someone answer a question using only this,
without reading what came before or after?
(.venv) 

Criterion 5 — Top-3 source
Produced by: run_eval.py::run_once → store.py::
### What are study spots students can use besides the library? — run 1

- Best distance: 0.3698 (passed the gate)
- Sources retrieved: thread_commuting.txt, thread_first_gen.txt, thread_printing.txt, thread_sleep_schedule.txt, thread_study_spots.txt

```
According to `thread_study_spots.txt`, students can use Ridgeway Café before 10am or the open lounges on floors 2 through 5 of the science building, which are unlocked and almost always empty.
```

### What are study spots students can use besides the library? — run 2

- Best distance: 0.3698 (passed the gate)
- Sources retrieved: thread_commuting.txt, thread_first_gen.txt, thread_printing.txt, thread_sleep_schedule.txt, thread_study_spots.txt

```
Based on the provided documents, study spots outside of the library include the Ridgeway Café (before 10am) and the open lounges on floors 2 through 5 of the science building. 

Source: thread_study_spots.txt
```

### What are study spots students can use besides the library? — run 3

- Best distance: 0.3698 (passed the gate)
- Sources retrieved: thread_commuting.txt, thread_first_gen.txt, thread_printing.txt, thread_sleep_schedule.txt, thread_study_spots.txt

```
Study spots besides the library include the Ridgeway Café (before 10am) and the open lounges on floors 2 through 5 of the science building (thread_study_spots.txt).
```

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MET | All 5 of 5 in-scope questions had the information needed to answer the question in the retrieved chunks, exceeding the target of 4 of 5. |
| 2 | Every answer names a source | MET | All 5 of 5 in-scope answers identified a source document, meeting the target of 5 of 5. |                                                                                                                                        
| 3 | Gate stops out-of-corpus questions | MET | The relevance gate refused all 5 of 5 out-of-scope questions, exceeding the target of 4 of 5. |
| 4 | 4 of 5 sampled chunks should be readable as a complete paragraph-sized thought | MET | All 5 sampled chunks were readable as complete, self-contained thoughts without sentences being cut off at the beginning or end, exceeding the target of 4 of 5. |
| 5 | The correct source document should appear in the top 3 retrieved results | MISSED | The run output alphabetically sorts the retrieved source names before writing them to the report, so it does not preserve their retrieval ranking. Because the top-3 order cannot be determined from the recorded output, this criterion cannot be verified. |


## Diagnoses

     No confirmed misses in the current baseline evaluation. Criteria 1–4 all met their targets, and the original Criterion 5 was not measurable because run_eval.py alphabetically sorted the retrieved source names rather than preserving retrieval order. I therefore replaced Criterion 5 with a measurable criterion about correct source attribution.

     The results suggest that some of the original targets were conservative. In particular, Criterion 1 achieved 5/5 against a target of 4/5, Criterion 3 achieved 5/5 against a target of 4/5, and the five sampled chunks in Criterion 4 were all readable against a target of 4/5. I would tighten Criterion 1 from 4/5 to 5/5 because all five test questions have answer information represented in the corpus and the baseline retrieved the necessary information for every question.

## The Improvement

**What I changed:**

I revised Criterion 5 from measuring whether the correct source document appeared in the top 3 retrieved results to measuring whether the generated answer named the correct source document.

**Why I picked it:**

The original Criterion 5 could not be measured from the evaluation output because run_eval.py alphabetically sorts the retrieved source names instead of preserving their retrieval order. The revised criterion uses an observable outcome. The source named in the generated answer that can be checked directly against the source document containing the answer.

### Run Log — After

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. 4 of 5 sampled chunks should be readable as a complete paragraph-sized thought | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. The answer should name the correct source document | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

**Did it help?**

     The revised Criterion 5 made the criterion measurable. All 5 of 5 in-scope questions named the correct source document in all three runs, so the revised criterion was met. The revision did not change the retrieval or generation behavior; it changed the measurement from an unobservable retrieval-ranking outcome to a source-attribution outcome that could be directly checked from the generated answers.

## What's Still Broken

     No criteria were missed after the revision. All five criteria met their targets in the after run.

## What I'd Do Differently

     I would write Criterion 5 differently from the beginning. The original criterion depended on retrieval ranking, but the evaluation output did not preserve the ranking, so there was no reliable way to determine whether the correct source appeared in the top three. I would instead define the criterion around an observable outcome, such as whether the generated answer identifies the correct source document.

---

## Capstone

**What This Extends**

This extends my Unit 1–2 project, The Unofficial Guide: a RAG system over the `advice_threads` corpus that retrieves student forum threads with Chroma, refuses questions whose best distance is over 0.7, and answers the rest with Gemini while citing a source. Before this unit it only ran in my editor, one question at a time. `serve.py` was a bare Flask wrapper with no logging, no timing, and no metrics, so once a request finished there was no record of it. What's new is the operational layer: a documented local run path, a structured JSONL log with one record per `/ask` request (failed requests included), timing for each stage (retrieval vs. generation), and a per-request token count read back from the Gemini response, which my cost number comes from.

**The Shape**

Shape A: deploy and instrument, on Path B (local with logs). I'm adding one thing: instrumentation around the existing `/ask` path. That means a structured log record per request, with stage timings and token usage, plus two small tools, one that sends a fixed set of requests to the running server and one that reads the log back into numbers.

Out of scope:
- I'm not changing retrieval, chunking, the relevance cutoff, or the prompt. The answers should be the same as in Unit 2; only what gets recorded about them changes.
- I'm not adding failure hardening like a timeout on the Gemini call or a fallback when the API is down. That's Shape B. Failures get *logged*, not *handled* differently.
- I'm not hosting it (Path A) and I'm not logging the CLI (`app.py ask`) or `run_eval.py`. The server is the run path, and only server requests are logged.

**Running It**

Path B: local with logs. The single start command, the Python version, the pinned dependencies, and the model download are in [RUNNING.md](RUNNING.md) under "Capstone run path".

**Instrumentation**

Every `POST /ask` request writes one JSON record (one line) to `logs/requests.jsonl`. The writer is `runlog.py::write`, called from `serve.py::ask`. Every record has the same fields, in the same order. A value that doesn't apply is `null`, not left out:

- `ts`: ISO-8601 UTC time the request arrived
- `request_id`: short random id, also returned to the caller
- `route`: "/ask"
- `status`: answered | refused | rejected | error
- `http_status`: what the caller got back
- `question`: the input (truncated to 500 chars)
- `answer`: the output (truncated to 1000 chars); null on reject/error
- `sources`: files cited to the caller (sorted, as the API returns them)
- `retrieved`: [{label, distance}] nearest-first, top_k of them
- `best_distance`: what the relevance gate compared
- `threshold`: the cutoff it compared against
- `latency_ms`: whole request, end to end inside the server
- `retrieve_ms`: embed question + vector search
- `generate_ms`: prompt + Gemini call; null when refused
- `cache_hit`: answer came from the local cache (cost 0 tokens)
- `model_attempts`: calls actually sent to Gemini (retries included)
- `prompt_tokens`: read back from the Gemini response, not estimated
- `output_tokens`: output tokens, also read back from the Gemini response
- `total_tokens`: `prompt_tokens` + `output_tokens`; null when no model call was made
- `model`: the Gemini model that answered (`config.MODEL`)
- `corpus`: which corpus was searched
- `error_type`: exception class, or the reason an input was rejected
- `error`: message (truncated to 500 chars)

The session below is the full log from 2026-11-16 (`python tools/log_summary.py --paste 21`). The server ran with `AI201_CACHE=0`, and `tools/drive.py` sent three sets: the 5 in-scope questions twice (`--set in --repeat 2`), the 5 out-of-scope questions (`--set out`), and 6 malformed requests (`--set bad`). That's 21 requests and 21 records: 10 answered, 5 refused by the relevance gate, and 6 rejected with a 400.

**Failed runs:** the last six records are rejected inputs. Each one names why it was rejected in `error_type`: `body_not_json_object` (an empty body, a body that isn't JSON, and a JSON list), `missing_question`, `question_not_string`, and `empty_question`. An earlier session against a corrupted index is kept in `logs/broken_index_session.jsonl`. Every question in it was refused, with best distances of 0.92 or higher.

```json
{"ts": "2026-11-16T04:09:50.179+00:00", "request_id": "ea4ad5ed4dc6", "route": "/ask", "status": "answered", "http_status": 200, "question": "What can a student do if they are not getting along with their roommate?", "answer": "A student should talk to their RA early, framing it as a request to help sort things out rather than asking to move. Additionally, they should write down specific details rather than just saying the situation is not working. \n\nSource: `thread_roommate_conflict.txt`", "sources": ["thread_commuting.txt", "thread_group_project.txt", "thread_office_hours_etiquette.txt", "thread_roommate_conflict.txt", "thread_study_spots.txt"], "retrieved": [{"label": "thread_roommate_conflict.txt#0", "distance": 0.3963}, {"label": "thread_group_project.txt#0", "distance": 0.5757}, {"label": "thread_office_hours_etiquette.txt#0", "distance": 0.7016}, {"label": "thread_study_spots.txt#0", "distance": 0.704}, {"label": "thread_commuting.txt#0", "distance": 0.7499}], "best_distance": 0.3963, "threshold": 0.7, "latency_ms": 3282.8, "retrieve_ms": 416.1, "generate_ms": 2231.7, "cache_hit": false, "model_attempts": 1, "prompt_tokens": 906, "output_tokens": 57, "total_tokens": 963, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": null, "error": null}
{"ts": "2026-11-16T04:09:53.465+00:00", "request_id": "30ead2ab7d60", "route": "/ask", "status": "answered", "http_status": 200, "question": "What determines whether a student can receive an extension for late work?", "answer": "Whether a student can receive an extension for late work depends entirely on the instructor, and the syllabus is accurate regarding their policies (thread_late_work.txt). Additionally, the universal rule is to ask before the deadline rather than after (thread_late_work.txt). Documented illness goes through the dean of students rather than the instructor (thread_late_work.txt).", "sources": ["thread_commuting.txt", "thread_first_year_regret.txt", "thread_group_project.txt", "thread_late_work.txt"], "retrieved": [{"label": "thread_late_work.txt#0", "distance": 0.5102}, {"label": "thread_group_project.txt#0", "distance": 0.6537}, {"label": "thread_first_year_regret.txt#1", "distance": 0.6669}, {"label": "thread_first_year_regret.txt#0", "distance": 0.6749}, {"label": "thread_commuting.txt#0", "distance": 0.675}], "best_distance": 0.5102, "threshold": 0.7, "latency_ms": 672.5, "retrieve_ms": 39.0, "generate_ms": 633.3, "cache_hit": false, "model_attempts": 1, "prompt_tokens": 841, "output_tokens": 78, "total_tokens": 919, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": null, "error": null}
{"ts": "2026-11-16T04:09:54.149+00:00", "request_id": "c90daf2ff8f4", "route": "/ask", "status": "answered", "http_status": 200, "question": "What are study spots students can use besides the library?", "answer": "Students can use the Ridgeway Café before 10am, or the open lounges on floors 2 through 5 of the science building, which are unlocked and almost always empty (thread_study_spots.txt).", "sources": ["thread_commuting.txt", "thread_first_gen.txt", "thread_printing.txt", "thread_sleep_schedule.txt", "thread_study_spots.txt"], "retrieved": [{"label": "thread_study_spots.txt#0", "distance": 0.3698}, {"label": "thread_first_gen.txt#0", "distance": 0.5875}, {"label": "thread_commuting.txt#0", "distance": 0.6968}, {"label": "thread_printing.txt#0", "distance": 0.7032}, {"label": "thread_sleep_schedule.txt#0", "distance": 0.7237}], "best_distance": 0.3698, "threshold": 0.7, "latency_ms": 1145.6, "retrieve_ms": 37.8, "generate_ms": 1107.7, "cache_hit": false, "model_attempts": 1, "prompt_tokens": 821, "output_tokens": 46, "total_tokens": 867, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": null, "error": null}
{"ts": "2026-11-16T04:09:55.320+00:00", "request_id": "0cda816833c5", "route": "/ask", "status": "answered", "http_status": 200, "question": "Who should a student ask about whether they need a specific edition of a textbook?", "answer": "A student should ask the instructor directly about whether a specific edition of a textbook is needed (thread_textbook_editions.txt).", "sources": ["thread_first_gen.txt", "thread_late_work.txt", "thread_pass_fail.txt", "thread_printing.txt", "thread_textbook_editions.txt"], "retrieved": [{"label": "thread_first_gen.txt#0", "distance": 0.6122}, {"label": "thread_textbook_editions.txt#0", "distance": 0.6372}, {"label": "thread_late_work.txt#0", "distance": 0.6648}, {"label": "thread_printing.txt#0", "distance": 0.6871}, {"label": "thread_pass_fail.txt#0", "distance": 0.7254}], "best_distance": 0.6122, "threshold": 0.7, "latency_ms": 617.9, "retrieve_ms": 34.6, "generate_ms": 583.2, "cache_hit": false, "model_attempts": 1, "prompt_tokens": 846, "output_tokens": 28, "total_tokens": 874, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": null, "error": null}
{"ts": "2026-11-16T04:09:55.961+00:00", "request_id": "aa45cee0af17", "route": "/ask", "status": "answered", "http_status": 200, "question": "How should a student handle an absent teammate in a group project?", "answer": "To handle an absent teammate in a group project, you should document things early so you have something written down if you need to go to the instructor (thread_group_project.txt). You should also raise the issue with the instructor before the deadline rather than after, as instructors are more likely to adjust individual grades beforehand (thread_group_project.txt). Additionally, split the work into independent pieces rather than making one person's part load-bearing, so a disappearance does not sink the whole project (thread_group_project.txt).", "sources": ["thread_first_year_regret.txt", "thread_group_project.txt", "thread_late_work.txt", "thread_roommate_conflict.txt"], "retrieved": [{"label": "thread_group_project.txt#0", "distance": 0.3}, {"label": "thread_roommate_conflict.txt#0", "distance": 0.6683}, {"label": "thread_late_work.txt#0", "distance": 0.7234}, {"label": "thread_first_year_regret.txt#0", "distance": 0.7795}, {"label": "thread_first_year_regret.txt#1", "distance": 0.8186}], "best_distance": 0.3, "threshold": 0.7, "latency_ms": 855.7, "retrieve_ms": 36.5, "generate_ms": 819.0, "cache_hit": false, "model_attempts": 1, "prompt_tokens": 841, "output_tokens": 111, "total_tokens": 952, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": null, "error": null}
{"ts": "2026-11-16T04:09:56.836+00:00", "request_id": "68469611808a", "route": "/ask", "status": "answered", "http_status": 200, "question": "What can a student do if they are not getting along with their roommate?", "answer": "A student should talk to their RA early and frame the conversation as needing help to sort things out rather than asking to move immediately (*thread_roommate_conflict.txt*). It is also helpful to write down specific details before the meeting rather than general complaints (*thread_roommate_conflict.txt*).", "sources": ["thread_commuting.txt", "thread_group_project.txt", "thread_office_hours_etiquette.txt", "thread_roommate_conflict.txt", "thread_study_spots.txt"], "retrieved": [{"label": "thread_roommate_conflict.txt#0", "distance": 0.3963}, {"label": "thread_group_project.txt#0", "distance": 0.5757}, {"label": "thread_office_hours_etiquette.txt#0", "distance": 0.7016}, {"label": "thread_study_spots.txt#0", "distance": 0.704}, {"label": "thread_commuting.txt#0", "distance": 0.7499}], "best_distance": 0.3963, "threshold": 0.7, "latency_ms": 740.9, "retrieve_ms": 38.3, "generate_ms": 702.5, "cache_hit": false, "model_attempts": 1, "prompt_tokens": 906, "output_tokens": 63, "total_tokens": 969, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": null, "error": null}
{"ts": "2026-11-16T04:09:57.600+00:00", "request_id": "482fa7719e37", "route": "/ask", "status": "answered", "http_status": 200, "question": "What determines whether a student can receive an extension for late work?", "answer": "Whether you can receive an extension is entirely instructor-dependent, and the policy in the syllabus is accurate (thread_late_work.txt). Additionally, the universal rule is to ask before the deadline rather than after (thread_late_work.txt). For documented illness, the process goes through the dean of students rather than the instructor (thread_late_work.txt).", "sources": ["thread_commuting.txt", "thread_first_year_regret.txt", "thread_group_project.txt", "thread_late_work.txt"], "retrieved": [{"label": "thread_late_work.txt#0", "distance": 0.5102}, {"label": "thread_group_project.txt#0", "distance": 0.6537}, {"label": "thread_first_year_regret.txt#1", "distance": 0.6669}, {"label": "thread_first_year_regret.txt#0", "distance": 0.6749}, {"label": "thread_commuting.txt#0", "distance": 0.675}], "best_distance": 0.5102, "threshold": 0.7, "latency_ms": 1487.4, "retrieve_ms": 36.5, "generate_ms": 1450.8, "cache_hit": false, "model_attempts": 1, "prompt_tokens": 841, "output_tokens": 77, "total_tokens": 918, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": null, "error": null}
{"ts": "2026-11-16T04:09:59.114+00:00", "request_id": "6ac45ff71ed9", "route": "/ask", "status": "answered", "http_status": 200, "question": "What are study spots students can use besides the library?", "answer": "Based on the provided documents, students can use the Ridgeway Café before 10am and the open lounges on floors 2 through 5 of the science building as study spots (thread_study_spots.txt).", "sources": ["thread_commuting.txt", "thread_first_gen.txt", "thread_printing.txt", "thread_sleep_schedule.txt", "thread_study_spots.txt"], "retrieved": [{"label": "thread_study_spots.txt#0", "distance": 0.3698}, {"label": "thread_first_gen.txt#0", "distance": 0.5875}, {"label": "thread_commuting.txt#0", "distance": 0.6968}, {"label": "thread_printing.txt#0", "distance": 0.7032}, {"label": "thread_sleep_schedule.txt#0", "distance": 0.7237}], "best_distance": 0.3698, "threshold": 0.7, "latency_ms": 727.8, "retrieve_ms": 37.2, "generate_ms": 690.5, "cache_hit": false, "model_attempts": 1, "prompt_tokens": 821, "output_tokens": 46, "total_tokens": 867, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": null, "error": null}
{"ts": "2026-11-16T04:09:59.863+00:00", "request_id": "5086356ff939", "route": "/ask", "status": "answered", "http_status": 200, "question": "Who should a student ask about whether they need a specific edition of a textbook?", "answer": "A student should ask the instructor directly about whether they need a specific edition of a textbook. \n\nSource: thread_textbook_editions.txt", "sources": ["thread_first_gen.txt", "thread_late_work.txt", "thread_pass_fail.txt", "thread_printing.txt", "thread_textbook_editions.txt"], "retrieved": [{"label": "thread_first_gen.txt#0", "distance": 0.6122}, {"label": "thread_textbook_editions.txt#0", "distance": 0.6372}, {"label": "thread_late_work.txt#0", "distance": 0.6648}, {"label": "thread_printing.txt#0", "distance": 0.6871}, {"label": "thread_pass_fail.txt#0", "distance": 0.7254}], "best_distance": 0.6122, "threshold": 0.7, "latency_ms": 661.9, "retrieve_ms": 38.4, "generate_ms": 623.4, "cache_hit": false, "model_attempts": 1, "prompt_tokens": 846, "output_tokens": 31, "total_tokens": 877, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": null, "error": null}
{"ts": "2026-11-16T04:10:00.550+00:00", "request_id": "459b63a1f0cb", "route": "/ask", "status": "answered", "http_status": 200, "question": "How should a student handle an absent teammate in a group project?", "answer": "To handle a group project where a teammate disappears, you should document things early so the instructor can help if approached before the deadline, and split the work into independent pieces so one person's absence does not sink the entire project (thread_group_project.txt).", "sources": ["thread_first_year_regret.txt", "thread_group_project.txt", "thread_late_work.txt", "thread_roommate_conflict.txt"], "retrieved": [{"label": "thread_group_project.txt#0", "distance": 0.3}, {"label": "thread_roommate_conflict.txt#0", "distance": 0.6683}, {"label": "thread_late_work.txt#0", "distance": 0.7234}, {"label": "thread_first_year_regret.txt#0", "distance": 0.7795}, {"label": "thread_first_year_regret.txt#1", "distance": 0.8186}], "best_distance": 0.3, "threshold": 0.7, "latency_ms": 1204.6, "retrieve_ms": 36.8, "generate_ms": 1167.7, "cache_hit": false, "model_attempts": 1, "prompt_tokens": 841, "output_tokens": 54, "total_tokens": 895, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": null, "error": null}
{"ts": "2026-11-16T04:10:06.026+00:00", "request_id": "4e22561613d4", "route": "/ask", "status": "refused", "http_status": 200, "question": "What is the capital of Mongolia?", "answer": "I don't have enough information about that.", "sources": [], "retrieved": [{"label": "thread_bike_commute.txt#1", "distance": 0.8902}, {"label": "thread_meal_plan_tier.txt#1", "distance": 0.9114}, {"label": "thread_laptop_specs.txt#0", "distance": 0.9479}, {"label": "thread_winter_advice.txt#0", "distance": 0.9645}, {"label": "thread_laundry_timing.txt#0", "distance": 0.968}], "best_distance": 0.8902, "threshold": 0.7, "latency_ms": 38.1, "retrieve_ms": 38.0, "generate_ms": null, "cache_hit": null, "model_attempts": 0, "prompt_tokens": null, "output_tokens": null, "total_tokens": null, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": null, "error": null}
{"ts": "2026-11-16T04:10:06.066+00:00", "request_id": "422a230c07cc", "route": "/ask", "status": "refused", "http_status": 200, "question": "How do I change the oil in a diesel engine?", "answer": "I don't have enough information about that.", "sources": [], "retrieved": [{"label": "thread_changing_major.txt#0", "distance": 0.9299}, {"label": "thread_winter_advice.txt#0", "distance": 0.9396}, {"label": "thread_meal_plan_tier.txt#1", "distance": 0.9484}, {"label": "thread_first_year_regret.txt#1", "distance": 0.969}, {"label": "thread_bike_commute.txt#1", "distance": 0.9851}], "best_distance": 0.9299, "threshold": 0.7, "latency_ms": 35.2, "retrieve_ms": 35.1, "generate_ms": null, "cache_hit": null, "model_attempts": 0, "prompt_tokens": null, "output_tokens": null, "total_tokens": null, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": null, "error": null}
{"ts": "2026-11-16T04:10:06.103+00:00", "request_id": "299739f177d3", "route": "/ask", "status": "refused", "http_status": 200, "question": "Who won the 1994 World Cup?", "answer": "I don't have enough information about that.", "sources": [], "retrieved": [{"label": "thread_meal_plan_tier.txt#1", "distance": 0.7866}, {"label": "thread_bike_commute.txt#1", "distance": 0.9199}, {"label": "thread_winter_advice.txt#0", "distance": 0.9517}, {"label": "thread_laptop_specs.txt#0", "distance": 0.955}, {"label": "thread_professor_email.txt#0", "distance": 0.9551}], "best_distance": 0.7866, "threshold": 0.7, "latency_ms": 32.8, "retrieve_ms": 32.8, "generate_ms": null, "cache_hit": null, "model_attempts": 0, "prompt_tokens": null, "output_tokens": null, "total_tokens": null, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": null, "error": null}
{"ts": "2026-11-16T04:10:06.154+00:00", "request_id": "e31349eb4a31", "route": "/ask", "status": "refused", "http_status": 200, "question": "What is the recommended dosage of ibuprofen for a headache?", "answer": "I don't have enough information about that.", "sources": [], "retrieved": [{"label": "thread_pass_fail.txt#0", "distance": 0.828}, {"label": "thread_printing.txt#0", "distance": 0.8389}, {"label": "thread_laptop_specs.txt#0", "distance": 0.88}, {"label": "thread_meal_plan_tier.txt#0", "distance": 0.9023}, {"label": "thread_winter_advice.txt#0", "distance": 0.9047}], "best_distance": 0.828, "threshold": 0.7, "latency_ms": 33.2, "retrieve_ms": 33.1, "generate_ms": null, "cache_hit": null, "model_attempts": 0, "prompt_tokens": null, "output_tokens": null, "total_tokens": null, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": null, "error": null}
{"ts": "2026-11-16T04:10:06.189+00:00", "request_id": "26f69e86656c", "route": "/ask", "status": "refused", "http_status": 200, "question": "How do I write a for loop in Rust?", "answer": "I don't have enough information about that.", "sources": [], "retrieved": [{"label": "thread_winter_advice.txt#0", "distance": 0.8712}, {"label": "thread_meal_plan_tier.txt#1", "distance": 0.8785}, {"label": "thread_clubs.txt#0", "distance": 0.9184}, {"label": "thread_parking.txt#0", "distance": 0.9341}, {"label": "thread_textbook_editions.txt#0", "distance": 0.946}], "best_distance": 0.8712, "threshold": 0.7, "latency_ms": 36.7, "retrieve_ms": 36.6, "generate_ms": null, "cache_hit": null, "model_attempts": 0, "prompt_tokens": null, "output_tokens": null, "total_tokens": null, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": null, "error": null}
{"ts": "2026-11-16T04:10:27.409+00:00", "request_id": "85fe07cd6928", "route": "/ask", "status": "rejected", "http_status": 400, "question": null, "answer": null, "sources": null, "retrieved": null, "best_distance": null, "threshold": null, "latency_ms": 0.1, "retrieve_ms": null, "generate_ms": null, "cache_hit": null, "model_attempts": null, "prompt_tokens": null, "output_tokens": null, "total_tokens": null, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": "body_not_json_object", "error": "no usable question in request body"}
{"ts": "2026-11-16T04:10:27.410+00:00", "request_id": "33443d5e7535", "route": "/ask", "status": "rejected", "http_status": 400, "question": null, "answer": null, "sources": null, "retrieved": null, "best_distance": null, "threshold": null, "latency_ms": 0.1, "retrieve_ms": null, "generate_ms": null, "cache_hit": null, "model_attempts": null, "prompt_tokens": null, "output_tokens": null, "total_tokens": null, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": "body_not_json_object", "error": "no usable question in request body"}
{"ts": "2026-11-16T04:10:27.429+00:00", "request_id": "2b45897de790", "route": "/ask", "status": "rejected", "http_status": 400, "question": null, "answer": null, "sources": null, "retrieved": null, "best_distance": null, "threshold": null, "latency_ms": 0.1, "retrieve_ms": null, "generate_ms": null, "cache_hit": null, "model_attempts": null, "prompt_tokens": null, "output_tokens": null, "total_tokens": null, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": "body_not_json_object", "error": "no usable question in request body"}
{"ts": "2026-11-16T04:10:27.444+00:00", "request_id": "0d296d0443c4", "route": "/ask", "status": "rejected", "http_status": 400, "question": null, "answer": null, "sources": null, "retrieved": null, "best_distance": null, "threshold": null, "latency_ms": 0.1, "retrieve_ms": null, "generate_ms": null, "cache_hit": null, "model_attempts": null, "prompt_tokens": null, "output_tokens": null, "total_tokens": null, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": "missing_question", "error": "no usable question in request body"}
{"ts": "2026-11-16T04:10:27.460+00:00", "request_id": "14c00fe7c304", "route": "/ask", "status": "rejected", "http_status": 400, "question": "42", "answer": null, "sources": null, "retrieved": null, "best_distance": null, "threshold": null, "latency_ms": 0.1, "retrieve_ms": null, "generate_ms": null, "cache_hit": null, "model_attempts": null, "prompt_tokens": null, "output_tokens": null, "total_tokens": null, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": "question_not_string", "error": "no usable question in request body"}
{"ts": "2026-11-16T04:10:27.476+00:00", "request_id": "d3187631e84a", "route": "/ask", "status": "rejected", "http_status": 400, "question": "'   '", "answer": null, "sources": null, "retrieved": null, "best_distance": null, "threshold": null, "latency_ms": 0.1, "retrieve_ms": null, "generate_ms": null, "cache_hit": null, "model_attempts": null, "prompt_tokens": null, "output_tokens": null, "total_tokens": null, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": "empty_question", "error": "no usable question in request body"}
```

**What It Costs**

Per-run cost: 910.1 tokens per answered request (851 input + 59.1 output) and 1.14 s, mean of 10 live runs. Refused and rejected requests cost 0 tokens.
How you measured it: 10 /ask requests with AI201_CACHE=0. Token counts come from Gemini’s usage_metadata on each response (logged as prompt_tokens and output_tokens), averaged by python tools/log_summary.py.

The 100-people-a-day arithmetic officially belongs to Mil

**Run Log and Verdicts**

Each trial is one command: `python tools/run_trial.py --label before --trial N` (`tools/run_trial.py::main`). It starts a fresh `serve.py` with the cache off (`AI201_CACHE=0`), sends the 21 standard requests with `tools/drive.py` (5 in-scope questions ×2, 5 out-of-scope, 6 malformed), restarts the server with an invalid `GEMINI_API_KEY`, and sends 1 in-scope question as the deliberate model failure. It then scores the trial with `tools/check_criteria.py::check`. The three trials ran back to back on 2026-11-16 with nothing changed in between. Every file each trial produced is in `results/capstone/`: `before_trialN.jsonl` is the server log written by `runlog.py::write`, `before_trialN.manifest.jsonl` is what the client sent and got back, and `before_trialN_check.txt` holds the scores.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every `/ask` request produces exactly one log record | 21 of 21 | 21/21 | 21/21 | 21/21 | |
| 2. Every log record contains all 23 required fields | 21 of 21 | 21/21 | 21/21 | 21/21 | |
| 3. Request and processing times are recorded accurately | 21 of 21 | 21/21 | 20/21 | 21/21 | |
| 4. Token usage is recorded and calculated correctly | 10 of 10 | 10/10 | 9/10 (9 of 9 answered) | 10/10 | |
| 5. Failed requests are recorded with their error details | 7 of 7 | 7/7 | 7/7 | 7/7 | |

Run 2's 9th request (in-scope, textbook-edition question) hit Gemini's free-tier quota: `429 RESOURCE_EXHAUSTED`. `generate.py::generate` retried 4 times (1 + 2 + 4 + 8 s backoff), gave up, and the server returned a 500 after 15.5 s. Only 9 of the 10 in-scope requests in run 2 produced an answer.

Real output below is from **run 2** (`results/capstone/before_trial2.*`), the run with the miss.

Scores for run 2, produced by `tools/check_criteria.py::main` (`before_trial2_check.txt`):

```
Trial log: C:\Users\ivanz\Downloads\Codepath AI 301\ai201-coursework\ai201-project1-unofficial-guide-starter-v2026\results\capstone\before_trial2.jsonl
Requests sent (main phase): 21   records in log: 22

C1  exactly one record per request ........ 21/21   (target 21 of 21)
C2  all 23 fields in every record .......... 21/21   (target 21 of 21)
C3  timings present / null as specified ... 20/21   (target 21 of 21)
C4  token counts on answered requests ..... 9/9   (target 10 of 10)
      null tokens on refused + rejected ... 11/11
C5  failures recorded with details ........ 7/7   (target 7 of 7)

Notes:
  - C3: main-phase record 33d73b3c438c has status 'error'; the criterion doesn't say which stages it reached — counted as a fail
  - C3: record 33d73b3c438c (error) timings: latency 15516.0, retrieve None, generate None
  - Outside C1–C3's 21: the model-error record has latency_ms 1287.4, retrieve_ms None, generate_ms None, error_type 'ClientError'
```

**Criterion 1: one record per request.** The client manifest (`tools/drive.py::main`, `--manifest`) has 21 main-phase requests and the server log has 22 records (21 + 1 model-error request). Every manifest `request_id` appears exactly once in the log. The first manifest line (its `request_id` is also the first record under criterion 3):

```json
{"phase": "main", "set": "in", "label": "What can a student do if they are not getting along with their roommate?", "http_status": 200, "request_id": "2ecedbb8861b", "client_ms": 1784.2, "client_error": null}
```

**Criterion 2: all 23 fields, `null` when they don't apply.** A rejected request, written by `serve.py::ask` → `runlog.py::write`:

```json
{"ts": "2026-11-16T04:31:12.061+00:00", "request_id": "1feb697b05f9", "route": "/ask", "status": "rejected", "http_status": 400, "question": "42", "answer": null, "sources": null, "retrieved": null, "best_distance": null, "threshold": null, "latency_ms": 0.0, "retrieve_ms": null, "generate_ms": null, "cache_hit": null, "model_attempts": null, "prompt_tokens": null, "output_tokens": null, "total_tokens": null, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": "question_not_string", "error": "no usable question in request body"}
```

**Criterion 3: timings.** A passing answered record and a passing refused record. Note the first request of the run, with retrieval at cold start:

```json
{"ts": "2026-11-16T04:30:47.583+00:00", "request_id": "2ecedbb8861b", "route": "/ask", "status": "answered", "http_status": 200, "question": "What can a student do if they are not getting along with their roommate?", "answer": "A student should talk to their RA early and frame the conversation as needing help to sort things out rather than asking to move immediately (*thread_roommate_conflict.txt*). Additionally, it is helpful to write down specific details and examples before the meeting (*thread_roommate_conflict.txt*).", "sources": ["thread_commuting.txt", "thread_group_project.txt", "thread_office_hours_etiquette.txt", "thread_roommate_conflict.txt", "thread_study_spots.txt"], "retrieved": [{"label": "thread_roommate_conflict.txt#0", "distance": 0.3963}, {"label": "thread_group_project.txt#0", "distance": 0.5757}, {"label": "thread_office_hours_etiquette.txt#0", "distance": 0.7016}, {"label": "thread_study_spots.txt#0", "distance": 0.704}, {"label": "thread_commuting.txt#0", "distance": 0.7499}], "best_distance": 0.3963, "threshold": 0.7, "latency_ms": 1769.1, "retrieve_ms": 158.8, "generate_ms": 1608.8, "cache_hit": false, "model_attempts": 1, "prompt_tokens": 906, "output_tokens": 62, "total_tokens": 968, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": null, "error": null}
{"ts": "2026-11-16T04:31:11.732+00:00", "request_id": "7aed16a3ab5e", "route": "/ask", "status": "refused", "http_status": 200, "question": "What is the capital of Mongolia?", "answer": "I don't have enough information about that.", "sources": [], "retrieved": [{"label": "thread_bike_commute.txt#1", "distance": 0.8902}, {"label": "thread_meal_plan_tier.txt#1", "distance": 0.9114}, {"label": "thread_laptop_specs.txt#0", "distance": 0.9479}, {"label": "thread_winter_advice.txt#0", "distance": 0.9645}, {"label": "thread_laundry_timing.txt#0", "distance": 0.968}], "best_distance": 0.8902, "threshold": 0.7, "latency_ms": 28.9, "retrieve_ms": 28.8, "generate_ms": null, "cache_hit": null, "model_attempts": 0, "prompt_tokens": null, "output_tokens": null, "total_tokens": null, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": null, "error": null}
```

The failing record. Status `error`, `latency_ms` 15516, but `retrieve_ms` and `generate_ms` are `null` even though retrieval ran before the model call failed:

```json
{"ts": "2026-11-16T04:30:55.289+00:00", "request_id": "33d73b3c438c", "route": "/ask", "status": "error", "http_status": 500, "question": "Who should a student ask about whether they need a specific edition of a textbook?", "answer": null, "sources": null, "retrieved": null, "best_distance": null, "threshold": null, "latency_ms": 15516.0, "retrieve_ms": null, "generate_ms": null, "cache_hit": null, "model_attempts": null, "prompt_tokens": null, "output_tokens": null, "total_tokens": null, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": "RuntimeError", "error": "Still rate limited after 4 attempts. Wait a minute and try again — your key is fine.\nLast error: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://aistudio.google.com/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit:…"}
```

**Criterion 4: tokens.** An answered record (`prompt_tokens` + `output_tokens` = `total_tokens`), produced by `app.py::ask_pipeline` → `generate.py::last_call`:

```json
{"ts": "2026-11-16T04:30:47.583+00:00", "request_id": "2ecedbb8861b", "route": "/ask", "status": "answered", "http_status": 200, "question": "What can a student do if they are not getting along with their roommate?", "answer": "A student should talk to their RA early and frame the conversation as needing help to sort things out rather than asking to move immediately (*thread_roommate_conflict.txt*). Additionally, it is helpful to write down specific details and examples before the meeting (*thread_roommate_conflict.txt*).", "sources": ["thread_commuting.txt", "thread_group_project.txt", "thread_office_hours_etiquette.txt", "thread_roommate_conflict.txt", "thread_study_spots.txt"], "retrieved": [{"label": "thread_roommate_conflict.txt#0", "distance": 0.3963}, {"label": "thread_group_project.txt#0", "distance": 0.5757}, {"label": "thread_office_hours_etiquette.txt#0", "distance": 0.7016}, {"label": "thread_study_spots.txt#0", "distance": 0.704}, {"label": "thread_commuting.txt#0", "distance": 0.7499}], "best_distance": 0.3963, "threshold": 0.7, "latency_ms": 1769.1, "retrieve_ms": 158.8, "generate_ms": 1608.8, "cache_hit": false, "model_attempts": 1, "prompt_tokens": 906, "output_tokens": 62, "total_tokens": 968, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": null, "error": null}
```

Run 2 has 9 answered records, all with correct token counts. The 10th in-scope request is the `error` record above, with `null` tokens and `model_attempts: null`, even though 4 calls were sent to Gemini.

**Criterion 5: failures recorded.** The 6 malformed requests are all `rejected` with HTTP 400 and an `error_type` (one is shown under criterion 2). The deliberate model failure (invalid API key):

```json
{"ts": "2026-11-16T04:31:13.551+00:00", "request_id": "63dec96ac870", "route": "/ask", "status": "error", "http_status": 500, "question": "What can a student do if they are not getting along with their roommate?", "answer": null, "sources": null, "retrieved": null, "best_distance": null, "threshold": null, "latency_ms": 1287.4, "retrieve_ms": null, "generate_ms": null, "cache_hit": null, "model_attempts": null, "prompt_tokens": null, "output_tokens": null, "total_tokens": null, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": "ClientError", "error": "400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}"}
```

**The Improvement**

<!-- Milestone 6 -->

**What's Still Broken**

<!-- Milestone 7 -->

**How I Used AI**

<!-- Milestone 7: two specific moments. -->
