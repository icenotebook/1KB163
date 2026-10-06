# Instructor notes for the pilot

This is a development notebook with teaching prompts, not an approved assessment or final student handout. Final timing, prerequisites, grading and delivery software remain to be agreed with the lecturer.

## Alignment with the supplied 1KB163 context

Outcomes 1 and 2: inspect data quality, implement preprocessing and judge distortion. Outcome 3: document sources, parameters, metadata and a reproducible sequence. Outcome 5: use comparable axes, baseline overlays and clearly labelled plots. Outcome 6: explain and justify conclusions. This pilot does not cover the modelling/validation methods in outcome 7.

## Suggested sequence

1. Ask students to sketch what they expect a baseline to contain. Inspect metadata, units, ordering and sampling interval before processing.
2. Use Raman as the main real-data example when the source file is available. Plot raw spectra and proposed baselines separately from corrected signals.
3. Predict how wavelet level, lambda and AsLS p influence results before changing one at a time. Avoid interpreting a smooth or flat output as proof of accuracy.
4. Use the synthetic spectrum to distinguish baseline RMSE from preservation of a specified peak-window area. Ask whether these criteria select the same method/settings.
5. Apply the workflow to XRF and discuss whether settings transfer. Signal scale, point spacing, peak width, sample and noise differ; lambda is not automatically transferable.
6. Have students record source, method, settings, evidence and limitations. Export one reproducible figure and a short justification.

## Student tasks

- Explain why baseline correction differs from smoothing/denoising.
- Compare estimated baselines and look for peak subtraction, negative excursions and edge effects. Negative values alone do not establish an error.
- Explore three lambda values and at least two wavelet levels; keep all other settings fixed and record why a setting is preferred.
- Compare synthetic baseline RMSE and peak-window area error. Explain the effect of noise and finite integration bounds.
- On real data, identify what cannot be validated without ground truth, replicates or an independent reference.
- Give another student enough metadata to reproduce one result.

## Instructor pilot log

Fill in after testing: elapsed time; setup difficulties; any missing data; confusing prompts; useful parameter ranges; evidence that intended chemistry/data-workflow reasoning occurred.

Before classroom delivery, obtain the real source data, verify the XRF calibration rows, select appropriate parameter ranges, and agree the student environment. Keep a solution notebook outside the student package. Generate a student version from the stable pilot rather than maintaining two divergent copies during development.
