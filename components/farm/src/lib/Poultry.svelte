<script>
	let { scale = 1 } = $props();
</script>

<svg
	xmlns="http://www.w3.org/2000/svg"
	xmlns:xlink="http://www.w3.org/1999/xlink"
	width="300"
	data-name="Ebene 2"
	viewBox="0 0 481.4 378.3"
>
	<defs>
		<style>
			.poultry-cls-1 {
				fill: #f4f0eb;
			}
			.poultry-cls-1,
			.poultry-cls-11,
			.poultry-cls-12,
			.poultry-cls-13,
			.poultry-cls-15,
			.poultry-cls-18,
			.poultry-cls-2 {
				stroke-linejoin: round;
			}
			.poultry-cls-1,
			.poultry-cls-11,
			.poultry-cls-12,
			.poultry-cls-15,
			.poultry-cls-18,
			.poultry-cls-2 {
				stroke: #1d1d1b;
			}
			.poultry-cls-2 {
				fill: #724137;
			}
			.poultry-cls-12,
			.poultry-cls-13,
			.poultry-cls-15,
			.poultry-cls-2 {
				stroke-linecap: round;
			}
			.poultry-cls-11 {
				fill: #2d2c57;
			}
			.poultry-cls-20 {
				fill: #1d1d1b;
			}
			.poultry-cls-12,
			.poultry-cls-18 {
				fill: #fff;
			}
			.poultry-cls-21 {
				fill: #c6c6c6;
			}
			.poultry-cls-13 {
				stroke: #fff;
			}
			.poultry-cls-13,
			.poultry-cls-15 {
				stroke-width: 2px;
				fill: none;
			}
			.poultry-cls-22 {
				fill: #dd0b19;
			}
		</style>
	</defs>
	<g data-name="All elements">
		<!-- Roof right -->
		<!-- <path d="m480.9 184.1-80.6 18.4L81.1 18.2 160.6.5z" class="poultry-cls-11" /> -->
		<path
			d="m81.1 18.2 {scale * 319.2} {scale * 184.3} 80.6 -18.4 {-scale * 319.2} {-scale * 184.3} z"
			class="poultry-cls-11"
		/>

		<!-- Roof left -->
		<path
			d="m.5 92.7 80.6-74.5 {scale * 319.2} {scale * 184.3}-79.5 73.8z"
			class="poultry-cls-11"
		/>
		<!-- Wall -->
		<path
			d="m.5,194.2 {scale * 320.3} {scale * 183.6} 0,{92.7 - 194.2} L.5 92.7z"
			class="poultry-cls-18"
		/>
		<!-- Windows -->
		<path d="M24.5 132.3v17.5l20 11.6v-17.6z" class="poultry-cls-18" />

		{#if scale < 0.4}
			<path d="M24.5 132.3v17.5l20 11.6v-17.6z" class="poultry-cls-18" />
		{:else if scale <= 0.5}
			<path
				d="M24.5 132.3v17.5l20 11.6v-17.6z m60.1 34.5v17.6l20 11.5v-17.6z"
				class="poultry-cls-18"
			/>
		{:else if scale <= 0.7}
			<path
				d="M24.5 132.3v17.5l20 11.6v-17.6z m60.1 34.5v17.6l20 11.5v-17.6z m60 34.6V219l20 11.6V213z"
				class="poultry-cls-18"
			/>
		{:else if scale <= 0.8}
			<path
				d="M24.5 132.3v17.5l20 11.6v-17.6z m60.1 34.5v17.6l20 11.5v-17.6z m60 34.6V219l20 11.6V213z m59.9 34.6v17.6l20 11.6v-17.6z"
				class="poultry-cls-18"
			/>
		{:else}
			<path
				d="M24.5 132.3v17.5l20 11.6v-17.6z m60.1 34.5v17.6l20 11.5v-17.6z m60 34.6V219l20 11.6V213z m59.9 34.6v17.6l20 11.6v-17.6z m59.8 34.8v17.6l20 11.5v-17.6z"
				class="poultry-cls-18"
			/>
		{/if}

		<g transform="translate({-(1 - scale) * 320.3},{-(1 - scale) * 183.6})">
			<!-- Opening -->
			<path d="M377.6 275.9v69.3l71-41.6v-69.2z" class="poultry-cls-1" />
			<path d="m391.8 267.8 56.3 32.8" class="poultry-cls-15" />
			<path
				d="M395.3 267.5c0-.4-.4-.6-.4-1.4s1.2-2.1 1.2-1.1l.2 2.2c0 .8-.4 1.4-.4 2.3l-.7 1.5c-.2-.4.3-1 .2-1s-.7.3-1 .6c0-.3.6-.7.8-.9l-1.3.6c.8-1 1.7-.8 1.7-.8z"
				style="fill:#f4db81"
			/>
			<path
				d="M391 267.6c.8.7.5.6 1.5.2l3.3-1.2c1-.3 2-1.5 2.2-2.6"
				style="stroke-linejoin:round;stroke-linecap:round;stroke:#010101;fill:#fff"
			/>
			<path
				d="m394.5 272.3 1.4 1c.6.4 2 1 2.7 1.6l.5.4c.8.7 2.3 1 3.3.6l3.4-1.2a4 4 0 0 0 2.2-2.7c.4-1.1.5-5.1.3-6.3q0-1.5-.7-1.7c-.3-.1-.4.6-.5.6q0-.2-.3-.2c-1.3.7-3.4 2.7-4 3l-3 1c-.2 0-4 1-4.8 2.2l-.6.7z"
				class="poultry-cls-2"
			/>
			<path d="M396.5 271.5q-.2 0-.2.2l.1.1.1-.1z" class="poultry-cls-21" />
			<path
				d="m394.7 271.3.3.6q.3.5 0 .6l-1.7.3c-.1-.2.8-1.5 1.4-1.5Z"
				style="stroke-linejoin:round;stroke:#010101;fill:#f4db81;stroke-width:.4px"
			/>
			<path
				d="M397.3 269c-1 .2-1.8.8-2.1 1s-.2-.8.3-.7c.1-.4.8-1 1-.6.7-.4.8.3.8.3"
				class="poultry-cls-22"
			/>
			<path
				d="m408.5 278.3 1.4 1c.6.4 2 1 2.8 1.6l.5.4c.8.7 2.4 1 3.4.6l3.4-1.2c1-.4 2-1.6 2.3-2.7s.5-5.2.3-6.4q-.2-1.4-.8-1.7c-.3-.2-.4.6-.5.6q0-.2-.2-.2c-1.4.7-3.5 2.7-4.2 3l-3 1c-.2.1-4 1.1-4.8 2.3l-.6.7z"
				class="poultry-cls-12"
			/>
			<path d="m410.6 277.5-.2.1v.2l.2-.1z" class="poultry-cls-20" />
			<path
				d="M408.7 277.3c.2 0 0 .4.3.6q.4.4 0 .6l-1.7.3c-.1-.2.8-1.5 1.4-1.5Z"
				style="stroke-linejoin:round;stroke-width:.4px;stroke:#010101;fill:#f4db81"
			/>
			<path
				d="M411.4 275q-1.6.4-2.2 1c-.6.6-.1-.8.4-.7 0-.4.8-1 1-.6.7-.5.8.3.8.3"
				class="poultry-cls-22"
			/>
			<path
				d="m418.6 286.6 1.4 1c.7.5 2.1 1.1 2.9 1.7l.5.5a4 4 0 0 0 3.6.6l3.6-1.3a4 4 0 0 0 2.3-2.8c.3-1.2.5-5.4.3-6.7q-.2-1.4-.8-1.8c-.3-.1-.4.7-.5.7q0-.2-.3-.2c-1.4.7-3.6 2.8-4.3 3l-3.2 1.2c-.1 0-4.2 1.1-5 2.3l-.6.8z"
				class="poultry-cls-12"
			/>
			<path d="m420.7 285.8-.2.1v.2h.1l.1-.2" class="poultry-cls-20" />
			<path
				d="m418.8 285.5.3.7q.4.3 0 .6l-1.8.4c-.1-.3.8-1.6 1.5-1.7Z"
				style="stroke-linejoin:round;stroke:#010101;fill:#f4db81;stroke-width:.42px"
			/>
			<path
				d="M421.6 283.2a5 5 0 0 0-2.3 1c-.3.4-.1-.8.4-.7 0-.4.8-1 1-.6.8-.5.9.3.9.3"
				class="poultry-cls-22"
			/>
			<path
				d="m431.7 293.7 1.5 1c.7.6 2.2 1.2 3 1.9l.5.4c1 .8 2.6 1 3.8.7l3.7-1.4c1.2-.4 1.6-1.7 1.8-2.9.2-1.3.5-5.7.3-7-.1-1 .3-1.7-.1-1.9s-.5.7-.6.7q0-.2-.3-.2c-1.5.7-3.8 3-4.5 3.2l-3.3 1.2c-.2 0-4.4 1.2-5.3 2.4l-.6.9z"
				class="poultry-cls-2"
			/>
			<path d="m433.8 293.2.1-.2v-.1l-.2.1" class="poultry-cls-21" />
			<path
				d="M431.9 292.6c.2 0 0 .4.3.6q.4.4 0 .7l-1.9.4c0-.3.9-1.7 1.6-1.7Z"
				style="stroke-linejoin:round;stroke:#010101;fill:#f4db81;stroke-width:.44px"
			/>
			<path
				d="M434.8 290.1q-1.7.5-2.3 1.2c-.6.7-.2-1 .4-.8 0-.5.8-1.2 1-.7.9-.5 1 .3 1 .3"
				class="poultry-cls-22"
			/>
			<path d="m411.1 256.7 36.9 20.9" class="poultry-cls-15" />
			<path
				d="M408.4 258c.6.5 2 1 2.8 1.7l.4.3c.8.7 2.3 1 3.2.6l3.3-1.2c1-.3 2-1.4 2.1-2.5.3-1 .5-4.9.3-6m-1 13.4 1.4.9c.5.5 1.9 1 2.6 1.6l.5.4c.8.7 2.3 1 3.3.6l3.4-1.2c1-.4 2-1.5 2.1-2.6.4-1.2.5-5 .3-6.3q-.1-1.3-.7-1.6c-.3-.2-.4.6-.5.6q0-.2-.3-.2c-1.3.7-3.4 2.6-4 2.9l-3 1c-.1.1-3.9 1-4.6 2.2l-.6.7z"
				class="poultry-cls-12"
			/>
			<path d="M421.5 263.5h-.1l-.1.1v.2q.2 0 .2-.2" class="poultry-cls-20" />
			<path
				d="m419.7 263.3.3.6q.3.3 0 .5l-1.7.4c-.1-.3.7-1.5 1.3-1.5Z"
				style="stroke-linejoin:round;stroke:#010101;fill:#f4db81;stroke-width:.39px"
			/>
			<path
				d="M422.2 261q-1.6.4-2 1c-.5.6-.2-.8.3-.7 0-.4.7-1 1-.5.7-.5.7.2.7.2"
				class="poultry-cls-22"
			/>
			<path
				d="m432.2 270.9 1.5 1c.6.4 2 1 2.7 1.6l.5.4a4 4 0 0 0 3.5.6l3.4-1.2c1-.4 1.7-1.6 1.9-2.7.3-1.6.3-5.3 0-6.5 0-.9.3-1.6 0-1.7-.4-.2-.5.6-.6.6q0-.2-.2-.2c-1.4.7-3.6 2.7-4.2 3l-3.1 1.1c-.2 0-4 1-4.9 2.2l-.6.8z"
				style="stroke-linejoin:round;stroke:#1d1d1b;fill:#724137;stroke-linecap:round;stroke-width:.81px"
			/>
			<path d="M434.3 270q-.2 0-.2.2v.2q.2 0 .2-.2z" class="poultry-cls-21" />
			<path
				d="M432.4 269.8c.2 0 0 .4.3.6q.4.5 0 .6l-1.7.4c-.2-.3.8-1.5 1.4-1.6Z"
				style="stroke-linejoin:round;stroke:#010101;fill:#f4db81;stroke-width:.4px"
			/>
			<path
				d="M435.1 267.5c-1 .2-1.9.8-2.2 1s-.1-.8.4-.7c0-.4.8-1 1-.6.7-.4.8.3.8.3"
				class="poultry-cls-22"
			/>
			<path d="m431 245.2 17.1 9.3" class="poultry-cls-15" />
			<path d="M448.6 303.6v-69.2l-72.3 41.8" style="stroke-linejoin:round;fill:none;stroke:#000" />
			<path
				d="m432.1 248 1.4 1c.6.5 2 1 2.8 1.7l.5.4c.8.7 2.4 1 3.4.6l3.4-1.2c1-.4 2-1.6 2.3-2.7s.5-5.3.3-6.5q-.2-1.5-.8-1.7c-.3-.1-.4.7-.5.7q0-.2-.2-.2c-1.4.6-3.5 2.6-4.2 2.9l-3 1.1c-.2 0-4.1 1-4.9 2.2l-.6.8z"
				class="poultry-cls-12"
			/>
			<path d="m434.2 247.3-.1-.1-.1.2v.1z" class="poultry-cls-20" />
			<path
				d="m432.3 247 .3.6q.4.4 0 .6l-1.8.4c0-.3.9-1.6 1.5-1.6Z"
				style="stroke-linejoin:round;stroke:#010101;fill:#f4db81;stroke-width:.4px"
			/>
			<path
				d="M435 244.7c-1 .2-1.9.8-2.2 1s-.2-.8.4-.7c0-.4.7-1 1-.6.7-.4.8.3.8.3"
				class="poultry-cls-22"
			/>
			<path
				d="M480.9 285.6V184.1l-81.4 18.1-78.7 74.1v101.5l27.9-15.8v-69.3l99.9-58.3v69.2z"
				class="poultry-cls-1"
			/>
			<path
				d="M330.6 301.2V373l70-40.6v-71.6z"
				style="stroke-linejoin:round;stroke:#1d1d1b;stroke-linecap:round;fill:#894e40"
			/>
			<path
				d="M384 294.7c-.7-3.7-2.7 2.4-3.3.6-.7-1.9-5.9 5.6-11.1 10-3.4 2.8-7.3 2.7-11.8 1.7h0s0-.8.8-2.5c1.3-3.4-2.4.4-2.4.4s-.6-5-2.6.4c-.5-1.4-3.7-4-3.8 2.7-3.3 2.4-5.5 8.8-3 8 7-2.7 4.2 3.4 7.4 8.4 3.4 5.3 12.4 9.1 23.7-1.1s7-24.9 6.2-28.6Z"
				class="poultry-cls-13"
			/>
			<path
				d="M362.4 336.8c2.1-.6 2.8-7.2 2.8-7.2m4.7 5c2.1-.5 2.8-7.1 2.8-7.1"
				class="poultry-cls-13"
			/>
		</g>
	</g>
</svg>

<style>
	svg {
		overflow: visible;
	}
</style>
