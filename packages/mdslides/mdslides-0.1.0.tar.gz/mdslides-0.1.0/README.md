# Description

`mdSlides` is a small utility for creating slideshows from markdown files. It is a wrapper around other tools
that actually generate the slides (currently only Pandoc) and handles setting up and passing the correct
command options to each tool.

Given a small Pandoc markdown file named simple.md,
```markdown
---
title  : Example Presentation
---

# First Slide

Text

# Second Slide

$\nabla \cdot \vec{E} = \frac{\rho}{\epsilon_0}$
```
and running `mdSlides` on it
```bash
$ mdSlides simple.md
```
will produce a directory named `simple` that contains a file named `index.html`. You can open the file
in a web browser to start the slide show.

`mdSlides` will also copy files that are needed for the slideshow, for example css files, images, etc, and
configure the slideshow to use the local files so that you can copy the directory to another computer (like
a web server) and it will still work.

Multiple "engines" are supported. The default engine uses [Pandoc](https://pandoc.org/) to output
a [slidy](https://github.com/slideshow-templates/slideshow-slidy) presentation. To see a list of
supported engines, run
```
$ mdSlides --list-engines
```
Only a few engines are currently supported, but others will be added in the future.

## Installing

You can install mdSlides with `pip`

```
pip install mdSlides
```

