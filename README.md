# CrossRefTag

To create `Cross-references` and `Chain Reference` Bibles by using the Biblical Terms information from [ParaTExt](www.paratext.org). This tool will attempt to automatically add cross-refences or footnotes for Biblical Terms by using the information available on the Biblical Terms in a ParaTExt project.

This tool can be incorporated in to ParaTExt as a check (cms) or as a command line tool.

## Pre-requisites

- ParaTExt 7/8 project (or files from a ParaTExt project)
- Biblical Terms must be marked

## How does it work

ParaTExt Biblical Terms information is stored in two files.

1. BiblicalTerms[i]ProjectCode[/i].xml
- This file has the Biblical Terms and it's renderings in the vernacular project.
1. ProjectBiblicalTerms.xml
- This file is static across all project (but the content may vary depending on the Biblical Term selected for the project). It has the Biblical Terms and the list of places it occur (this information is stored in a cryptic manner)

CrossRefTag will combine these files to determine the Biblical Terms entries for the project and then try to use that info to update the USFM files with the cross references.

We follow [Hitchhickers guide](http://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/creation.html#directory-layout) for packaging
