// Entry program for news-image-20261123 (Node 22, stdlib only).
// The rendered front page lives next to this file as entry.png;
// this program places a copy at <output>/entry.png, where <output>
// is /output inside the grader, or $MAKEFUN_OUTPUT_DIR when set.
// Local check:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const picture = join(here, 'entry.png');

if (!existsSync(picture)) {
  console.error('cannot find entry.png beside main.ts');
  process.exit(1);
}

const destination = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(destination, { recursive: true });
writeFileSync(join(destination, 'entry.png'), readFileSync(picture));
