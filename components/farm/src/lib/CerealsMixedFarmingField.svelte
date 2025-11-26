<script>
	const { row, y } = $props();

	// repeat after maxwidth
	const maxWidth = 10;
	let position = $derived(y >= maxWidth ? y % maxWidth : y);
</script>

{#if [4, 3, 2].includes(position)}
	<use href="#mixed-farming-salad" />
	{#if row % 4 === 0 && [2].includes(position)}
		<use href="#sheep-1" />
	{:else if (row - 1) % 5 === 0 && [3].includes(position)}
		<use href="#sheep-2" />
	{/if}
{:else if [1, 0].includes(position)}
	<use href="#cereals" />
{:else if [5, 6, 7, 8, 9].includes(position)}
	<use href="#mixed-farming-corn" />
{/if}
