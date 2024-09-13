# sopel-flipper

A Sopel plugin to flip (and mirror) text

## Installing

Releases are hosted on PyPI, so after installing Sopel, all you need is `pip`:

```shell
$ pip install sopel-flipper
```

## Using

Flip, roll, or mirror text with a CTCP ACTION (`/me` command) and Sopel will
output the transformation along with a suitable _kaomoji_.

```
* dgw flips the joint
<Sopel> (╯°□°）╯︵ ʇuᴉoɾ ǝɥʇ
* dgw rolls NoobGuy
<Sopel> (╮°-°)╯︵ ʎn⅁qooN NoobGuy ʎn⅁qooN NoobGuy ʎn⅁qooN (@_@;)
* dgw mirrors the quick brown fox
<Sopel> ╰( ⁰ ਊ ⁰ )━💨🪞 xoʇ nwoɿd ʞɔiup ɘ⑁Ɉ
```

Alternatively, use the `.flip`, `.roll`, or `.mirror` commands.

```
<dgw> .flip the joint
<Sopel> (╯°□°）╯︵ ʇuᴉoɾ ǝɥʇ
<dgw> .roll NoobGuy
<Sopel> (╮°-°)╯︵ ʎn⅁qooN NoobGuy ʎn⅁qooN NoobGuy ʎn⅁qooN (@_@;)
<dgw> .mirror the quick brown fox
<Sopel> ╰( ⁰ ਊ ⁰ )━💨🪞 xoʇ nwoɿd ʞɔiup ɘ⑁Ɉ
```

_Easter egg: Try `.flip a table`!_
