# [lexid][repo_ref]

`lexid` is a micro library to increment lexically ordered numerical ids.

Throughout the sequence of ids, this expression will always be true, whether you are dealing with integers or strings:

    older_id < newer_id

The left most character/digit is only used to maintain lexical order, so that the position in the sequence is maintained in the remaining digits.

Such ids can be useful as build or version numbers, which are often displayed by tooling which does not understand their correct ordering.

Project/Repo:

[![MIT License][license_img]][license_ref]
[![Supported Python Versions][pyversions_img]][pyversions_ref]
[![CalVer 2021.1006][version_img]][version_ref]
[![PyPI Version][pypi_img]][pypi_ref]
[![PyPI Downloads][downloads_img]][downloads_ref]

Code Quality/CI:

[![GitHub CI Status][github_build_img]][github_build_ref]
[![GitLab CI Status][gitlab_build_img]][gitlab_build_ref]
[![Type Checked with mypy][mypy_img]][mypy_ref]
[![Code Coverage][codecov_img]][codecov_ref]
[![Code Style: sjfmt][style_img]][style_ref]


|               Name               |    role           |      since       | until |
|----------------------------------|-------------------|------------------|-------|
| Manuel Barkhau (mbarkhau@gmail.com) | author/maintainer | 2020-09 | -     |


## Usage

```
$ pip install lexid
$ lexid_incr 1001
1002
$ lexid_incr 1999
22000
$ lexid_incr 1
22
$ lexid_incr 1 -n 100
22
..
28
29
330
331
...
398
399
4400
4401
...
```

In Python.

```
>>> import lexid
>>> lexid.incr("1")
'22'
>>> lexid.incr("0001")
'0002'
>>> lexid.incr("0999")
'11000'
```

To avoid possible zero truncation issues (e.g. with "0001" -> "1") and to reduce rollovers, start at a higher number:

```
>>> lexid.incr("1001")
'1002'
>>> lexid.incr("1002")
'1003'
>>> lexid.incr("1999")
'22000'
```


## Lexical Ids

The key thing to look at is how padding may eventually be exhausted.
In order to preserve lexical ordering, build numbers are incremented
in a special way. Examples will perhaps illustrate more clearly.

```python
"0001"
"0002"
"0003"
...
"0999"
"11000"
"11001"
...
"19998"
"19999"
"220000"
"220001"
```

What is happening here is that the left-most digit is incremented
early/preemptively. Whenever the left-most digit would change, the padding
of the id is expanded through a multiplication by 11.

```python
>>> prev_id  = "0999"
>>> num_digits = len(prev_id)
>>> num_digits
4
>>> prev_int = int(prev_id, 10)
>>> prev_int
999
>>> maybe_next_int = prev_int + 1
>>> maybe_next_int
1000
>>> maybe_next_id = f"{maybe_next_int:0{num_digits}}"
>>> maybe_next_id
"1000"
>>> is_padding_ok = prev_id[0] == maybe_next_id[0]
>>> is_padding_ok
False
>>> if is_padding_ok:
...     # normal case
...     next_id = maybe_next_id
... else:
...     # extra padding needed
...     next_int = maybe_next_int * 11
...     next_id  = str(next_int)
>>> next_id
"11000"
```

This behaviour ensures that the following semantic is always preserved:
`new_version > old_version`. This will be true, regardless of padding
expansion. To illustrate the issue this solves, consider what would happen
if we did not expand the padding and instead just incremented numerically.

```python
"0001"
"0002"
"0003"
...
"0999"
"1000"
...
"9999"
"10000"
```

Here we eventually run into a build number where the lexical ordering is
not preserved, since `"10000" > "9999" == False` (because the string `"1"`
is lexically smaller than `"9"`). With large enough padding this may be a
non issue, but it's better to not have to think about it.

Just as an example of why lexical ordering is a nice property to have,
there are lots of software which read git tags, but which have no logic to
parse version strings. This software can nonetheless order the version tags
correctly using commonly used lexical ordering. At the most basic
level it can allow you to use the UNIX `sort` command, for example to parse
VCS tags.


```shell
$ printf "v0.9.0\nv0.10.0\nv0.11.0\n" | sort
v0.10.0
v0.11.0
v0.9.0

$ printf "v0.9.0\nv0.10.0\nv0.11.0\n" | sort -n
v0.10.0
v0.11.0
v0.9.0

$ lexid_incr 0997 -n 5 | sort
0998
0999
11000
11001
11002
```

This sorting even works correctly in JavaScript!

```
> var versions = ["11002", "11001", "11000", "0999", "0998"];
> versions.sort();
["0998", "0999", "11000", "11001", "11002"]
```

[repo_ref]: https://github.com/mbarkhau/lexid

[github_build_img]: https://github.com/mbarkhau/lexid/workflows/CI/badge.svg
[github_build_ref]: https://github.com/mbarkhau/lexid/actions?query=workflow%3ACI

[gitlab_build_img]: https://gitlab.com/mbarkhau/lexid/badges/master/pipeline.svg
[gitlab_build_ref]: https://gitlab.com/mbarkhau/lexid/pipelines

[codecov_img]: https://gitlab.com/mbarkhau/lexid/badges/master/coverage.svg
[codecov_ref]: https://mbarkhau.gitlab.io/lexid/cov

[license_img]: https://img.shields.io/badge/License-MIT-blue.svg
[license_ref]: https://github.com/mbarkhau/lexid/blob/master/LICENSE

[mypy_img]: https://img.shields.io/badge/mypy-checked-green.svg
[mypy_ref]: https://mbarkhau.gitlab.io/lexid/mypycov

[style_img]: https://img.shields.io/badge/code%20style-%20sjfmt-f71.svg
[style_ref]: https://gitlab.com/mbarkhau/straitjacket/

[pypi_img]: https://img.shields.io/badge/PyPI-wheels-green.svg
[pypi_ref]: https://pypi.org/project/lexid/#files

[downloads_img]: https://pepy.tech/badge/lexid/month
[downloads_ref]: https://pepy.tech/project/lexid

[version_img]: https://img.shields.io/static/v1.svg?label=CalVer&message=2021.1006&color=blue
[version_ref]: https://pypi.org/project/pycalver/

[pyversions_img]: https://img.shields.io/pypi/pyversions/lexid.svg
[pyversions_ref]: https://pypi.python.org/pypi/lexid

