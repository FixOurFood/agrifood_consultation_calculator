import { format } from 'd3-format';

export const f = format('.1f');

// Format percentage
export const fp = format('.2p');

export function shuffleArray(array: number[]) {
	for (let i = array.length - 1; i > 0; i--) {
		const j = Math.floor(Math.random() * (i + 1));
		[array[i], array[j]] = [array[j], array[i]];
	}
}

export function reshape1DTo2D(arr: number[], x: number, y: number) {
	if (arr.length !== x * y) {
		throw new Error(`Array ${arr} length doesn't match dimensions`);
	}
	const result = [];
	for (let i = 0; i < x; i++) {
		result.push(arr.slice(i * y, (i + 1) * y));
	}
	return result;
}

export function appendY(...arrays: (number[][] | null)[]) {
	const nonNullArrays = arrays.filter((a) => a !== null);
	// Arrays must all have the same number of rows
	return nonNullArrays[0].map((_, i) => nonNullArrays.map((arr) => arr[i]).flat());
}

export function allocateToTargetSum(weights: number[], targetSum: number) {
	const total = weights.reduce((a, b) => a + b, 0);
	const normalized = weights.map((w) => w / total);

	const scaled = normalized.map((w) => w * targetSum);

	const intParts = scaled.map(Math.floor);

	const remainder = targetSum - intParts.reduce((a, b) => a + b, 0);

	const fracParts = scaled.map((v, i) => [i, v - intParts[i]]);

	fracParts.sort((a, b) => b[1] - a[1]);

	for (let i = 0; i < remainder; i++) {
		intParts[fracParts[i][0]] += 1;
	}

	return intParts;
}
