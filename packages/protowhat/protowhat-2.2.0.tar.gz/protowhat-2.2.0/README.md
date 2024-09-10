# protowhat

[![PyPI version](https://badge.fury.io/py/protowhat.svg)](https://badge.fury.io/py/protowhat)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fdatacamp%2Fprotowhat.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fdatacamp%2Fprotowhat?ref=badge_shield)

`protowhat` is a utility package required by `shellwhat` and `sqlwhat` packages, used for writing Submission Correctness Tests SCTs for interactive Shell and SQL exercises on DataCamp. It contains shared functionality related to SCT syntax, selectors and state manipulation.

- If you are new to teaching on DataCamp, check out https://instructor-support.datacamp.com.
- If you want to learn what SCTs are and how they work, visit [this article](https://instructor-support.datacamp.com/courses/course-development/submission-correctness-tests) specifically.
- For a deep dive in `protowhat`, consult https://protowhat.readthedocs.io.

## Installation

```
pyenv local 3.9.0
pip3.9 install protowhat   # install from pypi
make install            # install from source
```

## Testing

```
pip3.9 install -e .
pytest
```


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fdatacamp%2Fprotowhat.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fdatacamp%2Fprotowhat?ref=badge_large)