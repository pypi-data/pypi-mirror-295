# Markdown reference

[TOC]

## Headings

```markdown
# This is H1, the title of the page.

## This is H2, for page sections.

### This is H3, for subsections.

#### H4 through H6 are also possible, but should be used sparingly.
```

In addition to the standard headings, there is a special `subtitle` heading that's used to create a stylized, short phrase under the first heading. This is useful for product tag lines:

Analog-inspired parameterized drum synthesizer
{: .subtitle}

```
Analog-inspired parameterized drum synthesizer
{: .subtitle}
```

### This is H3

#### This is H4

##### This is H5

###### This is H6

## Inline text

Inline text can be formatted in several ways, such as **bold**, _italic_, **_bold and italic_**, ~~strikethrough~~, `monospace`, super^script^, sub~script~, ==mark==, ^^insert^^, and ++ctrl+alt+del++.

```markdown
You can use **bold**, _italic_, **_bold and italic_**, ~~strikethrough~~, and `monospace`.
```


## Links

You can create links to [internal pages](/bia/) and [external sites](https://noiseengineering.us).

You can also use [named links][winterbloom] when you reference the same link [multiple][winterbloom] [times]
[winterbloom].

[winterbloom]: https://winterbloom.com

Links are automatically created if you reference a full, valid URL, for example, https://winterbloom.com.

You can also create [links to headings in the page](#page). Each heading has a permalink styled as a `#` next to it.

```markdown
You can create links to [internal pages](/bia/) and
[external sites](https://noiseengineering.us).

You can also use [named links][winterbloom] when you
reference the same link [multiple][winterbloom] [times]
[winterbloom].

[winterbloom]: https://winterbloom.com

Links are automatically created if you reference a
full, valid URL, for example, https://winterbloom.com.

You can also create [links to headings in the page](#page).
Each heading has a permalink styled as a `#` next to it.
```


## Lists

Lists look like this:

-   Lists can be
-   created unordered
-   or ordered
    1. They can also be nested
    1. multiple times
        - and different styles can
        - be mixed as
    1. needed

```markdown
-   Lists can be
-   created unordered
-   or ordered
    1. They can also be nested
    1. multiple times
        - and different styles can
        - be mixed as
    1. needed
```

## Blockquotes

This is a blockquote:

> You can format a paragraph as a blockquote,
> and even extend it over multiple lines.
> You can use text formatting like **bold** and _italic_
> as well.
>
> Blockquotes can also span multiple paragraphs and such.

```markdown
> You can format a paragraph as a blockquote,
> and even extend it over multiple lines.
> You can use text formatting like **bold** and _italic_
> as well.
```

## Code

When referencing code in the middle of a paragraph, use `this syntax`.

```
For larger, multi-line blocks of
code, you use the fenced block
syntax.
```

````markdown
When referencing code in the middle of a paragraph, use `this syntax`.

```
For larger, multi-line blocks of
code, you use the fenced block
syntax.
```
````

## Math

You can generate formatted math formulae by using [LaTeX markup](https://en.wikibooks.org/wiki/LaTeX/Mathematics):

$$
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$

```
$$
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$
```

You can also use formatted math inline with paragraph text, for example:

The slope-intercept form of a straight line is \(y=mx+b\), where \(m\) is the slope (\(rise/run\)) and \(b\) is the y-intercept.

```markdown
The slope-intercept form of a straight line is \(y=mx+b\), where \(m\) is the slope (\(rise/run\)) and \(b\) is the y-intercept.
```

This functionality is provided through the [Arithmatex](https://facelessuser.github.io/pymdown-extensions/extensions/arithmatex/) extension and [MathJax](https://www.mathjax.org/). MathJax is a powerful math markup renderer with accessibility features.

## Tables

| Reference | Value  |
| --------- | ------ |
| C1, C2    | 10 uF  |
| C3 - C10  | 100 nF |
| R1, R2    | 100 kΩ |
| R3        | 10 kΩ  |

```markdown
| Reference | Value  |
| --------- | ------ |
| C1, C2    | 10 uF  |
| C3 - C10  | 100 nF |
| R1, R2    | 100 kΩ |
| R3        | 10 kΩ  |
```

## Admonitions

Admonitions are a [Markdown extension](https://python-markdown.github.io/extensions/admonition/) that add stylized callouts.

!!! note
    Admonitions allow you to draw attention to specific text.

!!! info
    There are different types of admonitions.

!!! tip
    There are different types of admonitions.

!!! success
    There are different types of admonitions.

!!! question
    There are different types of admonitions.

!!! warning
    There are different types of admonitions.

!!! failure
    There are different types of admonitions.

!!! danger
    There are different types of admonitions.

!!! bug
    There are different types of admonitions.

!!! example
    There are different types of admonitions.

!!! quote
    There are different types of admonitions.

!!! fairy
    There are different types of admonitions.

!!! note "Admonition titles"
    You can set the title of an admonition if you don't want to use the generic title.

!!! tip inline end "Inline admonitions"
    This is an inline admonition

Admonitions can be inlined next to content, if desired.  This is just filler text to give it something to wrap around. You can ignore the rest of this paragraph. Seriously. I mean it!

Example source:

```markdown
!!! note
    Admonitions allow you to draw attention to specific text.

!!! warning
    There are two different styles of admonitions: `note` and `warning`. More can be added by modifying the theme.

!!! note "Admonition titles"
    You can set the title of an admonition if you don't want t0 use the generic title.
```

## Definition lists

Definition lists are a Markdown extension that's useful for defining terms or creating a legend.

Pitch
: The pitch knob and CV input adjusts the pitch of the fundamental oscillator.
This is a `1 V / octave` standard input. The knob sums with the CV input.

Decay
: The decay knob and CV input adjust the decay for all oscillators. The knob offsets the CV input.

```markdown
Pitch
: The pitch knob and CV input adjusts the pitch of the fundamental oscillator.
This is a `1 V / octave` standard input. The knob sums with the CV input.

Decay
: The decay knob and CV input adjust the decay for all oscillators. The knob offsets the CV input.
```

## Keys

The [keys](https://facelessuser.github.io/pymdown-extensions/extensions/keys/) extension adds syntax to format text using the [&lt;kbd> element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/kbd). It's similar to inline code formatting, but is specifically useful for references physical inputs, outputs, knob, etc.

For example: Each oscillator has an individual envelope that is controlled by the ++"Attack"++, ++"Decay"++, and ++"Harm"++ controls. The noise envelope is also affected by the ++"Attack"++ knob.

```markdown
For example: Each oscillator has an individual envelope that is controlled by
the ++"Attack"++, ++"Decay"++, and ++"Harm"++ controls. The noise envelope is
also affected by the ++"Attack"++ knob.
```

Keys can of course be used for keyboard keys, and there's special cases for those that add helpful icons:

* ++alt++, ++left-alt++, ++right-alt++
* ++command++, ++left-command++, ++right-command++
* ++control++, ++left-control++, ++right-control++
* ++meta++, ++left-meta++, ++right-meta++
* ++option++, ++left-option++, ++right-option++
* ++shift++, ++left-shift++, ++right-shift++
* ++super++, ++left-super++, ++right-super++
* ++windows++, ++left-windows++, ++right-windows++
* ++arrow-left++, ++arrow-right++, ++arrow-up++, ++arrow-down++
* ++escape++, ++caps-lock++, ++tab++, ++backspace++, ++backtab++, ++enter++, ++num-enter++
* ++context-menu++, ++print-screen++, ++clear++, ++eject++
* ++insert++, ++delete++, ++home++, ++end++, ++page-up++, ++page-down++

And of course, key combinations are styled nicely, like ++ctrl+alt+delete++ and ++command+v++.

## Abbreviations

You can use abbreviations (HTML tag `<abbr>`). First, create an abbreviation definition like this:

```markdown
*[HTML]: Hyper Text Markup Language
*[W3C]:  World Wide Web Consortium
```

then, elsewhere in the document, write text such as:

```markdown
The HTML specification is maintained by the W3C.
```

Any instace of the abbreviations will automatically get rendered as such, for example:

The HTML specification is maintained by the W3C.

*[HTML]: Hyper Text Markup Language
*[W3C]:  World Wide Web Consortium

Abbreviations are case-sensitive, and will span on multiple words when defined as such. An abbreviation may also have an empty definition, in which case `<abbr>` tags will be added in the text but the title attribute will be omitted. The abbreviation definitions can be anywhere in the document.

## Footnotes

Footnotes work mostly like reference-style links, where you use a *marker* in the text that will become a superscript link, and a footnote *definition*:

```
That's some text[^1] with a footnote.

[^1]: This is the footnote.
```

> That's some text[^1] with a footnote.

[^1]: This is the footnote.

You can place the definition wherever, but they'll all end up at the bottom of the document.

## Images

Standard markdown images are rendered with nice spacing:

![An example image](images/example.webp)

```markdown
![An example image](images/example.webp)
```

But there's a few more tricks. You can pull an image to left or right of a body of text. For example:

![An image pulled to the right](images/example.webp){: align=right }

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

```markdown
![An image pulled to the right](images/example.webp){: align=right }

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod ...
```

You can also control the size of the images:

![small](images/example.webp){: .small }
![quarter](images/example.webp){: .quarter }
![half](images/example.webp){: .half }

```markdown
![small](images/example.webp){: .small }
![quarter](images/example.webp){: .quarter }
![half](images/example.webp){: .half }
```

Finally, the theme automatically inverts illustrations (`.svg`s) when dark mode is used. Toggle dark mode on and off to see the effect on the image below:

![Inverted in dark mode](images/interface-cutoff-formula.svg)

```markdown
![Inverted in dark mode](images/interface-cutoff-formula.svg)
```

You can prevent this by using `.no-invert`:

![Not inverted in dark mode](images/interface-cutoff-formula.svg){: .no-invert }

```markdown
![Not inverted in dark mode](images/interface-cutoff-formula.svg){: .no-invert }
```
