<script lang="ts">
	import { onMount } from 'svelte';
	import { Streamlit, type RenderData } from '$lib/streamlit.ts';

	import GridField from '$lib/GridField.svelte';

	let data: { [key: string]: number } = $state({});

	const onRender = (event: Event): void => {
		data = (event as CustomEvent<RenderData>).detail.args.data;
		// console.log(event.detail.args.data);
	};

	let height = $state(0);

	$effect(() => {
		Streamlit.setFrameHeight(height + 60);
	});

	onMount(async () => {
		Streamlit.setComponentReady();
		Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);
	});

	// $inspect(data);
</script>

<main bind:clientHeight={height}>
	<div class="figure">
		{#if Object.keys(data).length !== 0}
			<GridField
				totalEmissions={data.total_emissions}
				selfSufficiency={data.self_sufficiency}
				pigs={data.pigs}
				dairyHerd={data.dairy_herd}
				poultry={data.poultry}
				cattle={data.beef_herd}
				sheep={data.sheep}
				beccsOnPasture={data.beccs_on_pasture}
				pasture={data.total_pasture}
				additionalForest={data.additional_forest}
				silvoPasture={data.silvopasture}
				cereals={data.cereals}
				mixedFarming={data.total_mixed_farming}
				horticulture={data.horticulture}
				oilseeds={data.oilseeds}
				potatoes={data.potatoes}
				beccsArable={data.beccs_on_arable}
				otherArable={data.total_arable}
				agroForestry={data.agroforestry}
				peatland={data.restored_peatland}
			></GridField>
		{/if}
	</div>
</main>

<style>
	main {
		max-width: 1200px;
		margin: 0 auto;
		font-family: 'Source Sans Pro', sans-serif;
		font-size: 14px;
	}
	.figure {
		max-height: 100%;
		position: relative;
		margin-top: 50px;
	}
</style>
