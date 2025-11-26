<script>
	import Empty from './Empty.svelte';
	import * as c from './constants';
	const { row, index } = $props();

	// repeat after maxHeight
	const maxHeight = 9;

	let position = $derived(row >= maxHeight ? row % maxHeight : row);
</script>

{#if [0, 1, 2].includes(position)}
	<use href="#mixed-farming-salad" />
{:else if position === 3}
	<Empty fill={c.brownForest} stroke={c.brownForest} />
	{#if index % 2 === 0}
		<use href="#small-bush" />
	{:else}
		<use href="#big-bush" />
	{/if}
{:else if [4, 5, 6].includes(position)}
	<use href="#cereals" />
{:else if position === 8}
	<Empty fill={c.brownForest} stroke={c.brownForest} />
	{#if index % 2 === 0}
		<use href="#big-tree" />
	{:else}
		<use href="#small-tree" />
	{/if}
{:else}
	<Empty fill={c.brownForest} stroke={c.brownForest} />
{/if}

<!-- <text x="16" y="16" fill="red" font-size="6">{position}-{index}</text> -->
