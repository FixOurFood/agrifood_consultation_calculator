# farm component

A visualization component for the **UK as Farm** Streamlit app, written in Svelte.

To test the app from within the Streamlit App change the `build` path in `__init__.py` to use
the local development server.

For the data input from the Streamlit app, see `uk_as_farm.py`.

## Developing

Install dependencies with `npm install` (or `pnpm install` or `yarn`), to start the development server:

```sh
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create the production version of the component.

```sh
npm run build
```

You can preview the production build with `npm run preview`.

The generated files should be checked into the repository so that they get deployed along the other Python files.
