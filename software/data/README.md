# Dataset layout

```text
data/
  raw/<session_id>/        immutable videos/images plus session.json
  interim/<session_id>/    extracted frames and draft labels
  processed/<dataset_id>/  manifests that point to immutable source sessions
```

Do not commit recordings to Git. Keep a manifest with hashes and relative paths.
Split train/validation/test by whole `session_id`; adjacent frames from one video
must never cross splits.

Minimum `session.json` fields:

- session ID, wall-clock start, and monotonic timestamp origin;
- camera name, resolution, frame rate, and relevant exposure/focus settings;
- target objects and labels;
- lighting/background/distance/motion/occlusion conditions;
- software commit and configuration identity;
- consent/privacy note confirming no people or faces are target data.

