# tofurengo_js

Client-side JavaScript implementation of the Tofurengo glyph tag engine.
Provides tag parsing, normalization, and rendering utilities for web applications.

## Features

- Tag parsing with brace escaping
- Glyph normalization with dataset lookup
- Unicode rendering with base/variant selection
- Fully browser-compatible ES modules
- Zero external dependencies

## Directory Structure

```
tofurengo_js/
├── src/            # Main source code (ES modules)
├── tests/          # Unit tests
├── .gitignore      # Git ignore rules
├── LICENSE         # MIT License
├── README.md       # Documentation
└── package.json    # Package definition
```

## Installation

```
npm install tofurengo_js
```

## Usage Example

```
import { TagParser } from "tofurengo_js";

const out = TagParser.processPipeline("A {MJ000001}", (tag) => {
    return tag.glyphName;
});

console.log(out);
```

## License

MIT
