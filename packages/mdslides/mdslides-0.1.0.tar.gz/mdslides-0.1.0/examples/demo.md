---
title  : Example Presentation
subtitle : demo
---

# Markdown

`HTMLSlideShowUtils` uses pandoc to create HTML slides shows from markdown
files. You write your presentation in a file named `slides.md`, then run make,
and an HTML version is created.

Each slide is a section in the markdown file.  You can read more about
creating slides with pandoc on the
[website](http://pandoc.org/MANUAL.html#producing-slide-shows-with-pandoc)

Using markdown means your slides are in plain text, which means they are easy
to version control, and they are easy to edit with scripts.

# Images

Images are added using the standard markdown syntax. You can use
relative paths:

![](./images/html5-logo.png)

A URL:

![](https://upload.wikimedia.org/wikipedia/commons/9/92/LaTeX_logo.svg)

or absolute paths:

![](/home/cclark/Code/sync/projects/mdSlides/examples/images/vim-logo.png)


However, if you use an absolute path the you cannot copy your slides to another machine unless you copy the image to the same absolute path.

# Preprocessing

The `slides.md` file is preprocessed before running `pandoc`. The preprocessor contains
a macro expander that will replace macros that expand into various things. For example,
there is a macro that takes a shell command and expands to the output of the command.

Several macros are provided, and user defined macros can easily be added.

# Math

Probably the number one reason I ended up switching to writing my slide shows in Markdown
was for the ability to write LaTeX directly in the slide. For PowerPoint, I use
[IguanaTex](http://www.jonathanleroux.org/software/iguanatex/), which is a very
good plugin for creating images of LaTeX. The plugin allows images to be edited after
they are created, but it is still a hassle to modify several images at once.

By default, LaTeX math is rendered using MathJax:

$\nabla \cdot \vec{E} = \frac{\rho}{\epsilon_0}$

$\nabla \cdot \vec{B} = 0$

$\nabla \times \vec{E} = -\frac{\partial \vec{B}}{\partial t}$

$\nabla \times \vec{B} = \mu_0\left( \vec{J} + \epsilon_0\frac{\partial \vec{E}}{\partial t}\right)$

This looks pretty good, but it is not a LaTeX compiler, so LaTeX packages are not supported.

# Macros: Math

The `\mathimg` macro will create an image of some LaTeX code (using
[tex2im](https://github.com/CD3/tex2im)) and expand to markdown code that includes
the image that was created (if `tex2im` is not
installed it will replace the macro with a standard `$...$`).

For example: \mathimg{\sin(x) = \int \cos(x) dx}. This doesn't
look as good as MathJax for inline math, but it allows you to use arbitrary LaTeX packages.

For example, this

\\mathimg{g = \\SI{9.8}{\\meter\\per\\second\\squared}}

will produce this

\mathimg{g = \SI{9.8}{\meter\per\second\squared}}

Since MathJax does not support the `siunitx`, this is the only way to use the \SI command.
You can also make the image larger, which is not possible with MathJax.

For example, this

\\mathimg[height="300"]{\\Delta E = \\delta Q + \\delta W}

will produce this

\mathimg[height="300"]{\Delta E = \delta Q + \delta W}


# Macros: Shell

The `\\shell` macro will run a command and include its output. This is useful for command line demonstrations.  For example, this:

\`\`\`

\> ls

\\shell{ls}

\`\`\`

will produce this:

```
> ls
\shell{ls}
```

