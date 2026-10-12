// Backward-compatible entry point for the shared authoring layout audit.
process.env.LECTURE ||= '05';
require('../../../packages/web-deck/tests/authoring-layout.cjs');
