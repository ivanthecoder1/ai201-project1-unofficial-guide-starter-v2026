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

**Per run:** **910.1 tokens per answered request** (851 input + 59.1 output) and **1.14 s** end to end inside the server, the mean of 10 live answered requests (the logged session on 2026-11-16 above). Refused and rejected requests never reach Gemini, so they cost **0 tokens** (about 35 ms and under 1 ms respectively). The free tier's actual spend is **$0**. Tokens and seconds are the real cost here.

**How I measured it:** I started the server with the response cache off (`AI201_CACHE=0`) so every answer was a real Gemini call, and sent 10 in-scope requests with `tools/drive.py --set in --repeat 2`. The token counts are the ones Gemini reports on each response (`usage_metadata`), logged per request as `prompt_tokens` and `output_tokens` by `generate.py::last_call`, and averaged by `python tools/log_summary.py`. Nothing came from a pricing page. As a cross-check, the 59 answered requests across all six M5/M6 trials averaged 912 tokens. Input barely moves (851 every time, since the prompt is always 5 chunks + the question); output varies with the answer (28 to 111 tokens).

**A hundred people a day:** if each of 100 people asks one in-scope question:
- Tokens: 100 × 910.1 = **91,010 tokens/day** (100 × 851 = 85,100 input + 100 × 59.1 = 5,910 output).
- Server time: 100 × 1.14 s = **114 s/day**.

Refused questions would bring both numbers down. On the free tier that's still $0. The real limit isn't money, it's the per-minute quota. My trials hit `429 RESOURCE_EXHAUSTED` after about 18 calls in one minute, so 100 questions spread over a day is fine, but 20 people asking in the same minute would not be.

**Run Log and Verdicts**

Each trial is one command: `python tools/run_trial.py --label before --trial N` (`tools/run_trial.py::main`). It starts a fresh `serve.py` with the cache off (`AI201_CACHE=0`), sends the 21 standard requests with `tools/drive.py` (5 in-scope questions ×2, 5 out-of-scope, 6 malformed), restarts the server with an invalid `GEMINI_API_KEY`, and sends 1 in-scope question as the deliberate model failure. It then scores the trial with `tools/check_criteria.py::check`. The three trials ran back to back on 2026-11-16 with nothing changed in between. Every file each trial produced is in `results/capstone/`: `before_trialN.jsonl` is the server log written by `runlog.py::write`, `before_trialN.manifest.jsonl` is what the client sent and got back, and `before_trialN_check.txt` holds the scores.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every `/ask` request produces exactly one log record | 21 of 21 | 21/21 | 21/21 | 21/21 | MET |
| 2. Every log record contains all 23 required fields | 21 of 21 | 21/21 | 21/21 | 21/21 | MET |
| 3. Request and processing times are recorded accurately | 21 of 21 | 21/21 | 20/21 | 21/21 | MISSED |
| 4. Token usage is recorded and calculated correctly | 10 of 10 | 10/10 | 9/10 (9 of 9 answered) | 10/10 | MISSED |
| 5. Failed requests are recorded with their error details | 7 of 7 | 7/7 | 7/7 | 7/7 | MET |

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

**Verdicts**

| # | Verdict | How I decided |
|---|---|---|
| 1 | MET | 21/21 in all three runs. Every request in each run's client manifest has exactly one matching `request_id` in the server log, including the request that failed in run 2. |
| 2 | MET | 21/21 in all three runs. This one can't really fail: `runlog.py::write` builds every record from the fixed `FIELDS` list, so all 23 keys are always present. That makes the target too low (see below). |
| 3 | MISSED | The target is 21 of 21 in every run. Run 2 came out 20/21. The target has to hold in all three runs, not most of them. |
| 4 | MISSED | Run 2 has 9/10. My target and my reason both name the 10 uncached requests that should produce answers. Only 9 did, so a 10th token record doesn't exist. Counting only the requests that did answer (9 of 9) would quietly lower the target to whatever happened, so I count it against 10. |
| 5 | MET | 7/7 in all three runs. All 6 malformed requests were `rejected` with a 400 and an `error_type`, and the invalid-key request was an `error` with a 500, an `error_type`, and the `error` message. |

**Diagnosis**

Both misses are one problem, not two. In run 2, the 9th request (the textbook-edition question) failed in the **generation stage**, and the **logging on the error path** then lost most of what had happened.

- *Where it failed:* `generate.py::generate`. Gemini returned `429 RESOURCE_EXHAUSTED` (`generate_content_free_tier_requests`), the free tier's per-minute request quota. In the 60 seconds before it, 18 Gemini calls had succeeded: 10 from run 1 and 8 from run 2, because the trials ran back to back. The client-side limiter in `generate.py::_wait_for_slot` didn't prevent it, for two reasons. It allows 30 requests a minute (`config.REQUESTS_PER_MINUTE`), which is more than the real quota. And it only counts calls made by its own process, while each trial starts a new server, so it never saw run 1's 10 calls. On the 429, `generate()` retried 4 times with 1, 2, 4 and 8 s waits: 15 s in total, inside a quota window that is a full minute. Then it raised `RuntimeError`, and `serve.py::ask` returned a 500 after 15.5 s. Run 3 sent a similar burst without hitting the quota, so I can see the limit exists, but not exactly where it sits.
- *Why that cost criterion 4:* the 10th request never produced an answer, so there was no token record to count.
- *Why that cost criterion 3:* the stage timings and the attempt count live in the dict that `app.py::ask_pipeline` *returns*. When the pipeline raises instead of returning, that dict is lost, and `serve.py::ask`'s `except` branch only has the exception to log. So the error record says `retrieve_ms: null`, `generate_ms: null`, `model_attempts: null`, even though retrieval ran and 4 calls were sent to Gemini. The mechanism is that my instrumentation only records what the happy path hands back. The request where the log mattered most is the one where it recorded least. The same gap shows on the deliberate invalid-key request in every run: `retrieve_ms: null`, `model_attempts: null`.

**Targets set too low:** criteria 1, 2 and 5 were met in every run. Criterion 2 can't fail with this code, so it measures a guarantee rather than behaviour. If I wrote it again, I'd replace it with one about what's *in* the fields, e.g. that every `error` record has a numeric `retrieve_ms` and `model_attempts`, which is the gap this diagnosis found.

**The Improvement**

**What I changed:** the error path now logs how far a request got before it failed. `app.py::ask_pipeline` takes a `trace` dict and fills it in *as each stage finishes*: retrieval time and results, the gate's distance, then generation time and the model-attempt count, recorded in a `finally` so they're kept even when the Gemini call raises. `serve.py::ask` passes that dict in, and its `except` branch now writes `retrieve_ms`, `generate_ms`, `model_attempts`, `retrieved`, `best_distance` and `threshold` into the error record. Before, it wrote only the exception. `generate.py::reset_last_call` clears the per-thread usage first, so a failure can't report the previous request's numbers. The 23-field schema is unchanged, and nothing about retrieval, the gate, the prompt or the retry behaviour changed.

**Why I picked it:** it targets the mechanism behind criterion 3's miss: stage timings lived only in the dict `ask_pipeline` *returns*, so a request that raised lost them. It's also the part of the diagnosis that falls inside my declared scope. "Failures get logged, not handled differently" rules out changing the retry and backoff in `generate.py`, which is what actually lost run 2's answer and cost criterion 4.

One change to the scorer, made before the after-runs: `tools/check_criteria.py` used to fail every `error` record on criterion 3 automatically, because my criterion doesn't name that status. It now applies the criterion's own wording: a request that reaches retrieval must have a numeric `retrieve_ms`. Every error this system has produced happens in generation, after retrieval. I re-scored the three before-runs with the updated checker, and they come out exactly as before (run 2 is still 20/21 on criterion 3, still 9/10 on criterion 4).

**Run Log: Before** (2026-11-16, `results/capstone/before_trial*`)

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every `/ask` request produces exactly one log record | 21 of 21 | 21/21 | 21/21 | 21/21 | MET |
| 2. Every log record contains all 23 required fields | 21 of 21 | 21/21 | 21/21 | 21/21 | MET |
| 3. Request and processing times are recorded accurately | 21 of 21 | 21/21 | 20/21 | 21/21 | MISSED |
| 4. Token usage is recorded and calculated correctly | 10 of 10 | 10/10 | 9/10 | 10/10 | MISSED |
| 5. Failed requests are recorded with their error details | 7 of 7 | 7/7 | 7/7 | 7/7 | MET |

**Run Log: After** (same procedure, three runs back to back, `python tools/run_trial.py --label after --trial N`, `results/capstone/after_trial*`)

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every `/ask` request produces exactly one log record | 21 of 21 | 21/21 | 21/21 | 21/21 | MET |
| 2. Every log record contains all 23 required fields | 21 of 21 | 21/21 | 21/21 | 21/21 | MET |
| 3. Request and processing times are recorded accurately | 21 of 21 | 21/21 | 21/21 | 21/21 | MET |
| 4. Token usage is recorded and calculated correctly | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 5. Failed requests are recorded with their error details | 7 of 7 | 7/7 | 7/7 | 7/7 | MET |

Scores for after-run 2, from `tools/check_criteria.py::main` (`after_trial2_check.txt`):

```
Trial log: C:\Users\ivanz\Downloads\Codepath AI 301\ai201-coursework\ai201-project1-unofficial-guide-starter-v2026\results\capstone\after_trial2.jsonl
Requests sent (main phase): 21   records in log: 22

C1  exactly one record per request ........ 21/21   (target 21 of 21)
C2  all 23 fields in every record .......... 21/21   (target 21 of 21)
C3  timings present / null as specified ... 21/21   (target 21 of 21)
C4  token counts on answered requests ..... 10/10   (target 10 of 10; 10 of the in-scope requests were answered)
      null tokens on refused + rejected ... 11/11
C5  failures recorded with details ........ 7/7   (target 7 of 7)

Notes:
  - Outside C1–C3's 21: the model-error record has latency_ms 1263.9, retrieve_ms 157.8, generate_ms 1103.6, error_type 'ClientError'
```

The record the fix was aimed at, the deliberate model failure, in run 2 before and after. Before: `retrieve_ms`, `generate_ms` and `model_attempts` are all `null`. After: retrieval took 157.8 ms and found the right thread, and the one Gemini call failed 1103.6 ms later:

```json
{"ts": "2026-11-16T04:31:13.551+00:00", "request_id": "63dec96ac870", "route": "/ask", "status": "error", "http_status": 500, "question": "What can a student do if they are not getting along with their roommate?", "answer": null, "sources": null, "retrieved": null, "best_distance": null, "threshold": null, "latency_ms": 1287.4, "retrieve_ms": null, "generate_ms": null, "cache_hit": null, "model_attempts": null, "prompt_tokens": null, "output_tokens": null, "total_tokens": null, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": "ClientError", "error": "400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}"}
{"ts": "2026-11-16T04:43:27.512+00:00", "request_id": "4947438d107c", "route": "/ask", "status": "error", "http_status": 500, "question": "What can a student do if they are not getting along with their roommate?", "answer": null, "sources": null, "retrieved": [{"label": "thread_roommate_conflict.txt#0", "distance": 0.3963}, {"label": "thread_group_project.txt#0", "distance": 0.5757}, {"label": "thread_office_hours_etiquette.txt#0", "distance": 0.7016}, {"label": "thread_study_spots.txt#0", "distance": 0.704}, {"label": "thread_commuting.txt#0", "distance": 0.7499}], "best_distance": 0.3963, "threshold": 0.7, "latency_ms": 1263.9, "retrieve_ms": 157.8, "generate_ms": 1103.6, "cache_hit": false, "model_attempts": 1, "prompt_tokens": null, "output_tokens": null, "total_tokens": null, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": "ClientError", "error": "400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}"}
```

**Did it help?** Partly, and the after table makes it look better than it is.

- **What the fix did, measured directly:** the model-error record (the one request in every run that fails on purpose) has `retrieve_ms`, `generate_ms` and `model_attempts` in 3 of 3 after-runs, against 0 of 3 before. An error record now shows where the time went and how many calls were sent. That's the gap that hid run 2's four retries.
- **What the after table does *not* show:** criteria 3 and 4 went from MISSED to MET because no request *failed* in the after-runs, not because of the fix. The quota was hit again in after-run 2: `8` rate-limit retries in the server output (`after_trial2_server.txt`) across 4 requests. This time every one got through before running out of retries. The closest needed 4 attempts and 8 seconds:

```json
{"ts": "2026-11-16T04:43:14.972+00:00", "request_id": "a9c027367e84", "route": "/ask", "status": "answered", "http_status": 200, "question": "What are study spots students can use besides the library?", "answer": "According to the documents, study spots students can use besides the library include:\n\n* **Ridgeway Café** before 10am (thread_study_spots.txt).\n* **The science building**, which has open lounges on floors 2 through 5 that are unlocked and almost always empty (thread_study_spots.txt).", "sources": ["thread_commuting.txt", "thread_first_gen.txt", "thread_printing.txt", "thread_sleep_schedule.txt", "thread_study_spots.txt"], "retrieved": [{"label": "thread_study_spots.txt#0", "distance": 0.3698}, {"label": "thread_first_gen.txt#0", "distance": 0.5875}, {"label": "thread_commuting.txt#0", "distance": 0.6968}, {"label": "thread_printing.txt#0", "distance": 0.7032}, {"label": "thread_sleep_schedule.txt#0", "distance": 0.7237}], "best_distance": 0.3698, "threshold": 0.7, "latency_ms": 8040.3, "retrieve_ms": 30.9, "generate_ms": 8009.2, "cache_hit": false, "model_attempts": 4, "prompt_tokens": 821, "output_tokens": 71, "total_tokens": 892, "model": "gemini-3.5-flash-lite", "corpus": "advice_threads", "error_type": null, "error": null}
```

  One more 429 on that request, and run 2 would have repeated the before result for criterion 4. My change doesn't touch retrying, so criterion 4 is still exposed to the same failure. If it happens again, the difference is that the error record will now carry its timings and attempt count, so criterion 3 holds where it failed before.
- **A side effect:** retries now show up in the log on answered requests too (`model_attempts` 2–4 and a `generate_ms` of up to 8 s in after-run 2). That makes quota pressure visible without reading the server console.

**What's Still Broken**

No criterion was missed in the after-runs. That doesn't mean nothing is broken:

- **Criterion 4 is still exposed to the quota.** The improvement made failures *visible*; it didn't stop them. In after-run 2 the quota was hit again (8 retries across 4 requests), and one request needed all 4 attempts. One more 429 there and criterion 4 would have missed exactly as it did before. What I'd do: make the retry in `generate.py::generate` outlast the quota window (wait out the delay Gemini returns, with a total wait past 60 s instead of 15 s), and set `config.REQUESTS_PER_MINUTE` to the real free-tier limit rather than 30. Why I stopped: that's failure *handling*, which I put out of scope for shape A ("failures get logged, not handled differently"), and the unit's one improvement went to the logging gap that cost criterion 3.
- **Targets I set too low:** criterion 2 can't fail. `runlog.py::write` always writes all 23 keys, so it measured a guarantee in the code, not behaviour. I'd replace it with: *every `error` record has a numeric `retrieve_ms` and `model_attempts` (3 of 3 triggered failures)*. That's the gap the diagnosis actually found. I'd also tighten criterion 5 by adding the failure that really happened, a quota 429, to the deliberately triggered failures, instead of testing only a bad API key.

**What I'd do next:** if this were real, I'd extend the guide to more than one corpus, starting with indexing `campus_life` (courses, housing, dining, admin deadlines) alongside `advice_threads`, so it can answer a much wider range of student questions instead of refusing anything outside 23 forum threads. I'd do that first because the gate currently refuses every question outside those threads. The catch is that my 0.7 cutoff was measured on `advice_threads` alone, so each corpus would need its own relevance cutoff measured the same way, and my criteria and test questions would have to cover both corpora.

**How I Used AI**

**1. Coming up with the extension.** I asked Claude to help me choose and scope the capstone for this project. It read the repo, pointed out that `serve.py` had been deliberately left without logging or timing, and offered the three shapes. It recommended shape A on Path B, because the local embedding model plus Chroma wouldn't fit comfortably in a 512 MB free host. I took that, and it drafted the logging layer and the `drive.py`/`log_summary.py` tools. What came back wasn't all right. To check for regressions, it ran the starter's staff smoke test, which silently rebuilt my real index with fake embeddings. My next logged session refused all 10 in-scope questions. I caught it from my own log: every best distance was 0.92 or higher, and the roommate question retrieved the changing-major thread. I rebuilt the index and kept that session as `logs/broken_index_session.jsonl`. In Milestone 6 it offered two improvements. I chose logging the error path over fixing the retry, because the retry fix would have broken the out-of-scope line I'd already written.

**2. Refining the wording and organizing.** I asked Claude to help refine and organize my writing for the README and criteria. 