# Changelog
Changes related to the project will be documented here.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html)

## Unreleased

## [2.0.0-alpha.2] - 2019-14-01
### Added
- Google domain verification.(Note this is specific for my domain: slick.co.ke)

### Changed
- The structure of the old templates to match the structure of the
  other assets.

### Fixed
- Travis-CI not recognising the release naming scheme for alpha
  releases.
- Missing link in changelog to version 1.1.2.
- Stable section in README.md showing v1.1.2 as being in production.
- typos in link leading to github compare page between 2.0.0-alpha.1 and v1.1.2

## [2.0.0-alpha.1] - 2017-10-3
### Changed
- Moved the old files to /old folders in their respective locations.
- Updated the link to the old webpage as /old from /.
- the travis-ci configuration to include the new format for tags as
  part of the excluded tags.

## [1.1.2] - 2017-10-2
### Removed
- The changelog for the latest stable release from README.md.

### Changed
- Travis-CI configuration to eliminate redundancy.
- Travis-CI now ignores tags e.g. v1.2.0

## [1.1.1] - 2017-10-2
### Added
- A link in the README.md to compare master and dev branches
- A section in the README.md to dictate the current stable version.

### Fixed
- The link for comparing versions v1.1.0 and v1.0.0

## [1.1.0] - 2017-10-2
### Added
- A README.md file to give further descriptions on the project
- A MIT license in the file LICENSE.md
- Unit Testing capabilities using pytest. This includes a simple
  test case.
- Added travis-ci configuration to test, build and deploy the app
  to heroku.

### Changed
- Switched from using requirements.txt to using pipenv to handle dependencies.

## 1.0.0 - 2017-10-1
### Added
- This version represents the initial landing page for the website.
- Initially it was tagged as v1.0 but I changed the versioning to fit
  [Semantic Versioning](http://semver.org/spec/v2.0.0.html)
- I forgot the passphrase for the initial GPG key used, hence I was forced to
  generate a new one.

[2.0.0-alpha.2]: https://github.com/vickz84259/personal_website/compare/2.0.0-alpha.1...2.0.0-alpha.2
[2.0.0-alpha.1]: https://github.com/vickz84259/personal_website/compare/v1.1.2...2.0.0-alpha.1
[1.1.2]: https://github.com/vickz84259/personal_website/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/vickz84259/personal_website/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/vickz84259/personal_website/compare/v1.0.0...v1.1.0
