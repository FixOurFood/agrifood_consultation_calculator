<script lang="ts">
	import * as c from './constants.js';

	import { scaleLinear } from 'd3-scale';

	import Tooltip from './Tooltip.html.svelte';

	import AdditionalForest1Smallconifer from './AdditionalForest1_smallconifer.svelte';
	import AdditionalForest2Bigconifer from './AdditionalForest2_bigconifer.svelte';
	import AdditionalForest3Bigtree from './AdditionalForest3_bigtree.svelte';
	import AdditionalForest4Smalltree from './AdditionalForest4_smalltree.svelte';
	import AgroForestry from './AgroForestry.svelte';
	import BECCSArable from './BECCSArable.svelte';
	import BECCSPasture from './BECCSPasture.svelte';
	import Bigbush from './Bigbush.svelte';
	import Cattle1 from './Cattle1.svelte';
	import Cattle2 from './Cattle2.svelte';
	import Cereals from './Cereals.svelte';
	import CerealsMixedFarmingField from './CerealsMixedFarmingField.svelte';
	import Empty from './Empty.svelte';
	import Horticulture from './Horticulture.svelte';
	import MixedFarmingCorn from './MixedFarmingCorn.svelte';
	import MixedFarmingSalad from './MixedFarmingSalad.svelte';
	import Oilseed from './Oilseed.svelte';
	import OtherArable from './OtherArable.svelte';
	import Peatland1 from './Peatland1.svelte';
	import Peatland2 from './Peatland2.svelte';
	import Pig from './Pig.svelte';
	import Potatoes from './Potatoes.svelte';
	import Poultry1 from './Poultry1.svelte';
	import Poultry2 from './Poultry2.svelte';
	import Sheep1 from './Sheep1.svelte';
	import Sheep2 from './Sheep2.svelte';
	import Smallbush from './Smallbush.svelte';

	import DairyHerd from './DairyHerd.svelte';
	import Farmershouse from './Farmershouse.svelte';
	import Pigs from './Pigs.svelte';
	import Poultry from './Poultry.svelte';

	import { f, fp, shuffleArray, reshape1DTo2D, appendY, allocateToTargetSum } from './utils.js';

	let {
		totalEmissions = 10,
		selfSufficiency = 0.67,
		pigs = 9,
		dairyHerd = 3,
		poultry = 250,
		cattle = 10,
		sheep = 50,
		beccsOnPasture = 1,
		pasture = 1,
		additionalForest = 1,
		silvoPasture = 1,
		cereals = 1,
		mixedFarming = 1,
		horticulture = 1,
		oilseeds = 1,
		potatoes = 1,
		beccsArable = 1,
		otherArable = 1,
		agroForestry = 1,
		peatland = 1
	} = $props();

	// height (y) of lower field area
	const heightLower = 43;

	const spacer = Array(heightLower).fill([c.EMPTY_WHITE, c.EMPTY_WHITE]);
	const widthSpacer = spacer[0].length;

	const width = 56; //widthFieldA + widthFieldB + widthFieldC + 2 * spacer[0].length;
	const height = width;

	const heightUpper = height - heightLower;

	// The three fields are A, B, C from left to right.

	let sumFieldA = $derived(beccsOnPasture + pasture + additionalForest + silvoPasture);
	let sumFieldB = $derived(cereals + mixedFarming);
	let sumFieldC = $derived(
		horticulture + oilseeds + potatoes + beccsArable + otherArable + agroForestry + peatland
	);

	let [widthFieldA, widthFieldB, widthFieldC] = $derived(
		allocateToTargetSum([sumFieldA, sumFieldB, sumFieldC], width - 2 * widthSpacer)
	);

	let fieldAZeroes = $derived(
		[beccsOnPasture, pasture, additionalForest, silvoPasture].filter((v) => v === 0).length
	);

	let totalFieldASize = $derived(heightLower * widthFieldA - (4 - fieldAZeroes - 1) * widthFieldA);

	let [beccsPastureCount, pastureCount, additionalForestCount, silvoPastureCount] = $derived(
		allocateToTargetSum(
			[
				beccsOnPasture / sumFieldA,
				pasture / sumFieldA,
				additionalForest / sumFieldA,
				silvoPasture / sumFieldA
			],
			totalFieldASize
		)
	);

	// Might need adjustment to model max values.
	// https://www.gov.uk/government/statistics/livestock-populations-in-the-united-kingdom/livestock-populations-in-the-united-kingdom-at-1-june-2024

	let pigScale = scaleLinear().domain([0, 8]).range([0, 1]).unknown(0).clamp(true);
	let pigShare = $derived(pigScale(pigs));

	let dairyHerdScale = scaleLinear().domain([0, 4]).range([0, 1]).unknown(0).clamp(true);

	let dairyHerdShare = $derived(dairyHerdScale(dairyHerd));

	let poultryScale = scaleLinear().domain([0, 250]).range([0, 1]).clamp(true);
	let poultryShare = $derived(poultryScale(poultry));
	let cattleScale = $derived(
		scaleLinear()
			.domain([0, 15])
			.rangeRound([0, pastureCount > 20 ? 10 : Math.floor(pastureCount / 2)])
			.unknown(0)
			.clamp(true)
	);

	let cattleCount = $derived(cattleScale(cattle));

	let sheepScale = $derived(
		scaleLinear()
			.domain([0, 50])
			.rangeRound([0, pastureCount > 20 ? 10 : Math.floor(pastureCount / 2)])
			.unknown(0)
			.clamp(true)
	);
	let sheepCount = $derived(sheepScale(sheep));

	let fieldBZeroes = $derived([cereals, mixedFarming].filter((v) => v === 0).length);
	let fieldBSize = $derived(heightLower * widthFieldB - (2 - fieldBZeroes - 1) * widthFieldB);

	let [cerealsCount, mixedFarmingCount] = $derived(
		allocateToTargetSum([cereals / sumFieldB, mixedFarming / sumFieldB], fieldBSize)
	);

	let fieldCZeroes = $derived(
		[horticulture, oilseeds, potatoes, beccsArable, otherArable, agroForestry, peatland].filter(
			(v) => v === 0
		).length
	);
	let fieldCSize = $derived(heightLower * widthFieldC - (7 - fieldCZeroes - 1) * widthFieldC);

	let [
		horticultureCount,
		oilseedsCount,
		potatoesCount,
		beccsArableCount,
		otherArableCount,
		agroForestryCount,
		peatlandCount
	] = $derived(
		allocateToTargetSum(
			[
				horticulture / sumFieldC,
				oilseeds / sumFieldC,
				potatoes / sumFieldC,
				beccsArable / sumFieldC,
				otherArable / sumFieldC,
				agroForestry / sumFieldC,
				peatland / sumFieldC
			],
			fieldCSize
		)
	);

	// Allocate share of top areas to grid fields
	let [widthPigsDairy, widthHouse, widthPoultry] = allocateToTargetSum(
		[4 / 7, 2 / 7, 1 / 7],
		width
	);

	let top = appendY(
		reshape1DTo2D(
			Array(widthPoultry * (heightUpper - 1)).fill(c.MUD),
			heightUpper - 1,
			widthPoultry
		),
		reshape1DTo2D(
			Array(widthHouse * (heightUpper - 1)).fill(c.EMPTY_GREEN),
			heightUpper - 1,
			widthHouse
		),
		reshape1DTo2D(
			Array(widthPigsDairy * (heightUpper - 1)).fill(c.MUD),
			heightUpper - 1,
			widthPigsDairy
		)
	).concat(Array(width).fill(c.EMPTY_WHITE));

	let fieldPastureCattleSheep = $derived.by(() => {
		let pastureFieldValues = [
			Array(pastureCount - cattleCount - sheepCount).fill(c.PASTURE),
			Array(sheepCount).fill(c.SHEEP),
			Array(cattleCount).fill(c.TOTAL_CATTLE)
		].flat();
		shuffleArray(pastureFieldValues);
		return pastureFieldValues;
	});

	let fieldA = $derived(
		widthFieldA > 0
			? reshape1DTo2D(
					[
						Array(beccsPastureCount).fill(c.BECCS_ON_PASTURE),
						fieldPastureCattleSheep,
						Array(additionalForestCount).fill(c.ADDITIONAL_FOREST),
						Array(silvoPastureCount).fill(c.SILVOPASTURE)
					]
						.filter((v) => v.length !== 0)
						.map((a, index) => {
							if (a.length === 0) return [];
							else if (index < 4 - fieldAZeroes - 1) {
								return [a, Array(widthFieldA).fill(c.EMPTY_WHITE)].flat();
							} else return a;
						})
						.flat(),
					heightLower,
					widthFieldA
				)
			: null
	);

	let fieldB = $derived(
		widthFieldB > 0
			? reshape1DTo2D(
					[Array(cerealsCount).fill(c.CEREALS), Array(mixedFarmingCount).fill(c.MIXED_FARMING)]
						.filter((v) => v.length !== 0)
						.map((a, index) => {
							if (a.length === 0) return [];
							else if (index < 2 - fieldBZeroes - 1) {
								return [a, Array(widthFieldB).fill(c.EMPTY_WHITE)].flat();
							} else return a;
						})
						.flat(),
					heightLower,
					widthFieldB
				)
			: null
	);

	let fieldC = $derived(
		widthFieldC > 0
			? reshape1DTo2D(
					[
						Array(horticultureCount).fill(c.HORTICULTURE),
						Array(oilseedsCount).fill(c.OILSEEDS),
						Array(potatoesCount).fill(c.POTATOES),
						Array(beccsArableCount).fill(c.BECCS_ON_ARABLE),
						Array(otherArableCount).fill(c.OTHER_ARABLE),
						Array(agroForestryCount).fill(c.AGROFORESTRY),
						Array(peatlandCount).fill(c.PEATLAND)
					]
						.filter((v) => v.length !== 0)
						.map((a, index) => {
							if (a.length === 0) return [];
							else if (index < 7 - fieldCZeroes - 1) {
								return [a, Array(widthFieldC).fill(c.EMPTY_WHITE)].flat();
							} else return a;
						})
						.flat(),
					heightLower,
					widthFieldC
				)
			: null
	);

	let grid = $derived(top.concat(appendY(fieldC, spacer, fieldB, spacer, fieldA)).flat());

	let tooltipEvent: MouseEvent | null = $state(null);
	let tooltipId: number | null = $state(null);
</script>

<div style="visibility: hidden; position: absolute;">
	<svg id="pasture" viewBox="0 0 39 23">
		<polygon
			points="0,11.5 19.5,23 39,11.5 19.5,0"
			width="39"
			height="23"
			fill={c.greenPasture}
			stroke={c.greenPasture}
		></polygon>
	</svg>
</div>

{#if tooltipEvent !== null && ![null, c.EMPTY_WHITE, c.MUD].includes(tooltipId)}
	<Tooltip event={tooltipEvent}>
		<div>
			{#if tooltipId === c.BECCS_ON_PASTURE}
				BECCS on pasture {f(beccsOnPasture)} Mha
			{:else if tooltipId === c.PASTURE}
				<div>Pasture {f(pasture)} Mha</div>
			{:else if tooltipId === c.TOTAL_CATTLE || tooltipId === c.SHEEP}
				<div>Total Cattle {f(cattle)} mln</div>
				<div>Sheep {f(sheep)} mln</div>
			{:else if tooltipId === c.ADDITIONAL_FOREST}
				Additional Forest {f(additionalForest)} Mha
			{:else if tooltipId === c.SILVOPASTURE}
				Silvopasture {f(silvoPasture)} Mha
			{:else if tooltipId === c.CEREALS}
				Cereals {f(cereals)} Mha
			{:else if tooltipId === c.MIXED_FARMING}
				Mixed Farming {f(mixedFarming)} Mha
			{:else if tooltipId === c.HORTICULTURE}
				Horticulture {f(horticulture)} Mha
			{:else if tooltipId === c.OILSEEDS}
				Oilseeds {f(oilseeds)} Mha
			{:else if tooltipId === c.POTATOES}
				Potatoes {f(potatoes)} Mha
			{:else if tooltipId === c.BECCS_ON_ARABLE}
				BECCS on Arable {f(beccsArable)} Mha
			{:else if tooltipId === c.OTHER_ARABLE}
				Other Arable {f(otherArable)} Mha
			{:else if tooltipId === c.AGROFORESTRY}
				Agroforestry {f(agroForestry)} Mha
			{:else if tooltipId === c.PEATLAND}
				Restored peatland {f(peatland)} Mha
			{:else if tooltipId === c.PIGS}
				Pigs {f(pigs)} mln
			{:else if tooltipId === c.POULTRY}
				Poultry {f(poultry)} mln
			{:else if tooltipId === c.DAIRY_HERD}
				Dairy Herd {f(dairyHerd)} mln
			{/if}
		</div>
	</Tooltip>
{/if}

<div>
	<svg viewBox="0 0 {width * 39} {height * 23}" width="100%" height="100%">
		<!-- Earthy bottom layer -->
		<polygon
			id="earth"
			points="
		0,{(height / 2) * 23}
		0,{(height / 2) * 23 + 20}
		{(width / 2) * 39},{height * 23 + 20}
		{width * 39},{(height / 2) * 23 + 20}
		{width * 39},{(height / 2) * 23}
		"
			fill={c.earthyBrown}
			stroke-width="2"
			stroke="black"
		></polygon>

		<!-- Black outline and pasture green background -->
		<polygon
			points="
			0,{(height / 2) * 23} 
			{(width / 2) * 39},{height * 23}
			{width * 39},{(height / 2) * 23}
			{(width / 2) * 39},0"
			fill={c.greenPasture}
			stroke-width="2"
			stroke="black"
		></polygon>

		{#each grid as id, index (index)}
			{@const x = Math.floor(index / width)}
			{@const y = index % height}
			<!-- svelte-ignore a11y_no_static_element_interactions -->
			<!-- svelte-ignore a11y_mouse_events_have_key_events -->
			<svg id="grid-{index}" data-x={x} data-y={y} viewBox="0 0 39 23" width="39" height="23">
				<g
					transform="translate({(width - y - 1) * 19.5 + x * 19.5} 
									 {(width - y) * -11.5 + x * 11.5 + height * 11.5})"
					onmouseenter={(event) => {
						tooltipEvent = event;
						tooltipId = id;
					}}
					onmouseout={() => {
						tooltipEvent = null;
						tooltipId = null;
					}}
				>
					{#if id === c.MUD}/
						<Empty fill={c.dirtyBrown} stroke={c.dirtyBrown} />
					{:else if id === c.BECCS_ON_PASTURE}
						<use href="#beccs-on-pasture" />
					{:else if id === c.PASTURE}
						<use href="#pasture" />
					{:else if id === c.TOTAL_CATTLE}
						{#if x % 2 === 0}
							<use href="#cattle-1" />
						{:else}
							<use href="#cattle-2" />
						{/if}
					{:else if id === c.SHEEP}
						<use href="#sheep-1" />
					{:else if id === c.ADDITIONAL_FOREST}
						{@const randomTree = Math.random()}
						{#if randomTree <= 0.2}
							<use href="#small-conifer" />
						{:else if randomTree <= 0.4}
							<use href="#big-conifer" />
						{:else if randomTree <= 0.6}
							<use href="#big-tree" />
						{:else if randomTree <= 0.8}
							<use href="#small-tree" />
						{/if}
					{:else if id === c.SILVOPASTURE}
						{@const randomTree = Math.random()}
						{#if randomTree <= 0.1}
							<use href="#small-conifer" />
						{:else if randomTree <= 0.2}
							<use href="#big-conifer" />
						{:else if randomTree <= 0.3}
							<use href="#big-tree" />
						{:else if randomTree <= 0.4}
							<use href="#small-tree" />
						{:else if randomTree <= 0.5}
							<Cattle1 />
						{:else if randomTree <= 0.6}
							<Cattle2 />
						{:else if randomTree <= 0.7}
							<Sheep1 />
						{/if}
					{:else if id === c.CEREALS}
						<use href="#cereals" />
					{:else if id === c.MIXED_FARMING}
						<CerealsMixedFarmingField row={x} y={y - widthFieldC - widthSpacer} />
					{:else if id === c.HORTICULTURE}
						<use href="#horticulture" />
					{:else if id === c.OILSEEDS}
						<use href="#oilseed" />
					{:else if id === c.POTATOES}
						<use href="#potatoes" />
					{:else if id === c.BECCS_ON_ARABLE}
						<use href="#beccs-arable" />
					{:else if id === c.OTHER_ARABLE}
						<use href="#other-arable" />
					{:else if id === c.AGROFORESTRY}
						<AgroForestry row={x} {index} />
					{:else if id === c.PEATLAND}
						{#if x % 2 === 0}
							<use href="#peatland-1" />
						{:else}
							<use href="#peatland-2" />
						{/if}
					{:else if id === c.EMPTY_WHITE}
						<Empty />
					{/if}

					<!-- <text x="16" y="16" fill="red" font-size="6">{index}-{x}-{y}</text> -->
				</g>
			</svg>
		{/each}
		{#if pigShare > 0}
			<!-- svelte-ignore a11y_no_static_element_interactions -->
			<!-- svelte-ignore a11y_mouse_events_have_key_events -->
			<g
				transform="translate(210,-230)"
				onmouseenter={(event) => {
					tooltipEvent = event;
					tooltipId = c.PIGS;
				}}
				onmouseleave={() => {
					tooltipEvent = null;
					tooltipId = null;
				}}
			>
				<Pigs scale={pigShare} />
			</g>
		{/if}
		{#if dairyHerdShare > 0}
			<!-- svelte-ignore a11y_no_static_element_interactions -->
			<!-- svelte-ignore a11y_mouse_events_have_key_events -->
			<g
				transform="translate(500,-220)"
				onmouseenter={(event) => {
					tooltipEvent = event;
					tooltipId = c.DAIRY_HERD;
				}}
				onmouseleave={() => {
					tooltipEvent = null;
					tooltipId = null;
				}}
			>
				<DairyHerd scale={dairyHerdShare} />
			</g>
		{/if}
		{#if poultryShare > 0}
			<!-- svelte-ignore a11y_no_static_element_interactions -->
			<!-- svelte-ignore a11y_mouse_events_have_key_events -->
			<g
				transform="translate({(width / 2) * 39 - 100},{(-height / 2) * 23 + 60})"
				onmouseenter={(event) => {
					tooltipEvent = event;
					tooltipId = c.POULTRY;
				}}
				onmouseleave={() => {
					tooltipEvent = null;
					tooltipId = null;
				}}
			>
				<Poultry scale={poultryShare} />
			</g>
		{/if}
		<g transform="translate(820,-400)">
			<AdditionalForest2Bigconifer />
		</g>
		<g transform="translate(790,-390)">
			<AdditionalForest1Smallconifer />
		</g>
		<g transform="translate(850,-500)">
			<Farmershouse />
		</g>
	</svg>
</div>

<div>
	<div>
		<p>Emissions (Mt CO₂eq/year): Total <strong>{f(totalEmissions)}</strong></p>
		<p>Self-sufficiency <strong>{fp(selfSufficiency)}</strong></p>
	</div>
	<div>
		<details>
			<summary>Legend</summary>
			<span>
				<svg height="5" viewBox="0 -10 39 23" style="display: inline;">
					<AdditionalForest3Bigtree />
				</svg>
				<svg height="4" viewBox="0 -10 39 23" style="display: inline;">
					<AdditionalForest4Smalltree />
				</svg>
				Additional Forest
			</span>

			<span>
				<svg height="9" viewBox="0 0 39 23" style="display: inline;">
					<Cereals />
				</svg>
				<svg height="8" viewBox="0 -15 39 23" style="display: inline;">
					<AdditionalForest4Smalltree />
				</svg>
				<svg height="9" viewBox="0 0 39 23" style="display: inline;">
					<MixedFarmingSalad />
				</svg>
				Agroforestry
			</span>

			<span>
				<svg height="9" viewBox="0 0 39 23" style="display: inline;">
					<BECCSArable />
				</svg>
				BECCS on Arable
			</span>

			<span>
				<svg height="10" viewBox="0 0 39 23" style="display: inline;">
					<BECCSPasture />
				</svg>
				BECCS on pasture
			</span>

			<span>
				<svg height="9" viewBox="0 0 39 23" style="display: inline;">
					<Cereals />
				</svg>
				Cereals
			</span>

			<span>
				<svg height="10" viewBox="0 0 39 23" style="display: inline;">
					<Cattle2 />
				</svg>
				Dairy Herd
			</span>

			<span>
				<svg height="12" viewBox="0 -5 39 23" style="display: inline;">
					<Horticulture />
				</svg>
				Horticulture
			</span>

			<span>
				<svg height="10" viewBox="0 0 39 23" style="display: inline;">
					<MixedFarmingSalad />
				</svg>
				<svg height="10" viewBox="0 0 39 23" style="display: inline;">
					<MixedFarmingCorn />
					<Sheep1 />
				</svg>
				Mixed Farming
			</span>

			<span>
				<svg height="10" viewBox="0 0 39 23" style="display: inline;">
					<Oilseed />
				</svg>
				Oilseeds
			</span>

			<span>
				<svg height="10" viewBox="0 0 39 23" style="display: inline;">
					<OtherArable />
				</svg>
				Other Arable
			</span>

			<span>
				<svg height="10" viewBox="0 0 39 23" style="display: inline;">
					<use href="#pasture" />
				</svg>
				Pasture
			</span>

			<span>
				<svg height="10" viewBox="0 0 39 23" style="display: inline;">
					<Pig />
				</svg>
				Pigs
			</span>

			<span>
				<svg height="10" viewBox="0 0 39 23" style="display: inline;">
					<Potatoes />
				</svg>
				Potatoes
			</span>

			<span>
				<svg height="10" viewBox="0 0 39 23" style="display: inline;">
					<Poultry2 />
				</svg>
				<svg height="10" viewBox="0 0 39 23" style="display: inline;">
					<Poultry1 />
				</svg>
				Poultry
			</span>

			<span>
				<svg height="15" viewBox="0 -5 39 23" style="display: inline;">
					<Peatland1 />
				</svg>
				<span style="display: none;"><Peatland2 /></span>
				Restored Peatland
			</span>

			<span>
				<svg height="12" viewBox="0 0 39 23" style="display: inline;">
					<Sheep2 />
				</svg>
				<svg height="12" viewBox="0 0 39 23" style="display: inline;">
					<Sheep1 />
				</svg>
				Sheep
			</span>

			<span>
				<svg height="8" viewBox="0 -5 39 23" style="display: inline;">
					<AdditionalForest1Smallconifer />
				</svg>
				<svg height="10" viewBox="0 0 39 23" style="display: inline;">
					<Cattle1 />
				</svg>
				Silvopasture
			</span>

			<span>
				<svg height="10" viewBox="0 0 39 23" style="display: inline;">
					<g transform="translate(-10,10)">
						<Cattle2 />
					</g>
				</svg>
				<svg height="10" viewBox="0 0 39 23" style="display: inline;">
					<g transform="translate(-10,10)">
						<Cattle1 />
					</g>
				</svg>
				Total Cattle
			</span>
		</details>
	</div>
</div>

<style>
	svg {
		overflow: visible;
		position: relative;
		z-index: 999;
	}
	polygon#earth {
		filter: drop-shadow(6px 6px 5px rgba(0, 0, 0, 0.4));
	}
	details span {
		display: inline-block;
		margin-block-end: 1em;
		margin-inline-end: 1em;
	}
</style>
