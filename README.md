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
