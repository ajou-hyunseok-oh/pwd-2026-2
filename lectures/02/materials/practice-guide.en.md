# Week 2 — SvelteKit Portfolio Practice

Use Svelte 5 and SvelteKit to build a mini portfolio, track the source in GitHub and deploy it to Vercel. This archive contains the actual course practice project, including server routes. It is separate from the HTML/React examples used to explain browser concepts.

## Run the supplied source

Install Node.js 24, which includes npm. Extract the archive, open a terminal in the `pwd-week2` directory and run:

```sh
node -v
npm -v
npm ci
npm run dev
```

Open the local URL printed by Vite. Stop the server with Ctrl+C. If PowerShell blocks the npm script launcher, use `npm.cmd` and `npx.cmd`.

The supplied source is already a SvelteKit project. Do not run a project generator inside it. When starting a new project for the guided exercise, the course uses `npx sv@0.17.0 create pwd-week2`, the minimal template, JavaScript with JSDoc, npm, and the Prettier, ESLint, Vitest and Playwright add-ons. See the Korean README for the full step-by-step implementation.

## Files and behavior

| Route or file | Purpose |
| --- | --- |
| `src/routes/+layout.svelte` | Shared navigation and the current page, rendered through `children` |
| `/` | Name input updates a greeting; a button shows a random message |
| `/about` | Introduction and learning topics |
| `/api/projects` | Server endpoint returning three projects as JSON |
| `/projects` | A load function fetches the API; the page renders `Card` components |
| `/projects/[slug]` | Server load selects detail data; an unknown slug returns 404 |
| `/projects/memo` | Textarea with explicit Save and restoration from localStorage after reload |
| `src/lib/Card.svelte` | A card receiving `title`, `summary` and `href` props |

Timetable Helper and Image Gallery are descriptive detail pages, not complete timetable or gallery applications. The memo is stored in the current browser’s localStorage when Save is pressed. Unsaved edits are not restored after reload. The project includes SSR, API handling and server data loading; it is not configured as a static-only export.

## GitHub and Vercel

Create your own GitHub repository and push this project to it. Do not include `node_modules`, `.svelte-kit`, secrets or local environment files. The included `.gitignore` supplies the project’s exclusions.

In Vercel, import your repository, select the SvelteKit project directory and confirm the SvelteKit preset. Use Node.js 24.x and keep the automatically configured output directory. Add environment variables only if your own implementation requires them. Deploy and inspect the build log. The source uses `adapter-auto` to select the supported deployment adapter.

Check Home, About, Projects, the detail routes and memo persistence on the deployed site. Push another committed change and verify the new deployment. Copy the actual Production URL from your project dashboard; no particular `vercel.app` hostname is guaranteed. Preview and Production deployments depend on branch and project settings.

Submit your GitHub repository URL and Vercel Production URL. Use the deadline stated in the lecture assignment slide. This source archive does not establish a different deadline.

## Checks

```sh
npm run check
npm run build
```

These commands check the Svelte source and build the application. They do not prove that a Vercel deployment or GitHub integration has completed. Test the listed interactions in the browser as well. The project also includes lint and test commands; inspect their output rather than assuming a build runs every check.

Official references: [SvelteKit routing](https://svelte.dev/docs/kit/routing), [loading data](https://svelte.dev/docs/kit/load), [SvelteKit on Vercel](https://vercel.com/docs/frameworks/full-stack/sveltekit).
