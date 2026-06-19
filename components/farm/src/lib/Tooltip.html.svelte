<!--
  @component
  Generates a hover tooltip. It creates a snippet with an exposed variable via `let:detail` that contains information about the event. 
  Use the snippet to populate the body of the tooltip using the exposed variable `detail`.
Adapted from offsetCake

The MIT License (MIT)

Copyright (c) 2024 Michael Keller

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

  -->
<script>
	/**
	 * @typedef {Object} Props
	 * @property {MouseEvent} event - The mouse event that triggered the tooltip.
	 * @property {number} [offset=40] - A y-offset from the hover point, in pixels.
	 * @property {import('svelte').Snippet} [children]
	 */

	/** @type {Props} */
	let { event, offset = 40, children } = $props();
</script>

{#if event.offsetX !== undefined && event.offsetY !== undefined}
	<div
		class="tooltip"
		style="
      top:{event.offsetY + offset}px;
      left:{event.offsetX}px;
    "
	>
		{@render children?.()}
	</div>
{/if}

<style>
	.tooltip {
		position: absolute;
		min-width: 50px;
		border: 1px solid #ccc;
		font-size: 13px;
		background: rgba(255, 255, 255, 0.85);
		/* transform: translate(-50%, -100%); */
		padding: 5px;
		z-index: 99999;
	}
</style>
