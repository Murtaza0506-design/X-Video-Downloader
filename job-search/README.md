# Job search workspace

A working folder for one job search, run as a repeatable loop rather than a
pile of one-off applications. Everything here is plain text so it diffs,
travels, and can be edited by hand.

## The loop

1. **Profile** — `profile/cv.md` holds the master CV; `profile/target.md`
   holds what we are actually aiming at (role family, level, location,
   sector, salary floor, dealbreakers). Nothing downstream works until
   these two are real.
2. **Source** — find openings that match `target.md`. Each one gets a folder
   under `roles/<company>-<role>/` with the job description saved verbatim
   as `jd.md`.
3. **Score** — before writing anything, judge the fit honestly against
   `target.md` and the CV. A weak fit gets dropped here, not after an hour
   of writing. Record the verdict in `roles/<...>/fit.md`.
4. **Tailor** — for a role that survives scoring, produce a tailored CV and
   a cover letter in that role's folder, built from the master CV. Never
   invent experience; reorder, re-weight, and re-word what is already true.
5. **Track** — add a row to `tracker.csv` on submission and update its
   `status` as things move.
6. **Follow up** — the tracker's `next_action` and `next_action_date`
   columns are the queue. Work them.

## Rules this workspace runs by

- **No fabrication.** Tailoring means emphasis and vocabulary, not invented
  employers, dates, tools, or metrics. A CV that wins an interview it can't
  survive has cost you time, not saved it.
- **No mass auto-apply.** Volume spam is what makes application inboxes
  useless and it gets candidates filtered. This workspace is built for a
  smaller number of genuinely-fitting applications, each actually tailored.
- **The job description is evidence.** Save it verbatim; postings get taken
  down, and the wording is what the screen is run against.
- **Honest scoring.** The point of step 3 is to say no. If everything scores
  well, the scoring is broken.

## Layout

```
profile/cv.md        master CV, the single source of truth
profile/target.md    what we are aiming at
tracker.csv          one row per application
templates/           starting points for tailored CVs, letters, outreach
reference/           notes on the target market
roles/               one folder per opening
```
