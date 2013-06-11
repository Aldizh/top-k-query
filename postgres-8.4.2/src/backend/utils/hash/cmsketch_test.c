// Test code for your CountMin sketch.  We will test other cases than the ones presented here

#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>

#include "utils/cmsketch.h"

void expect_value(uint32_t expected, uint32_t found, char* tag);

void expect_value(uint32_t expected, uint32_t found, char* tag) {
	if (expected != found) {
		printf("ERROR: [%s] Expected %d found %d\n", tag, expected, found);
		exit(-1);
	}
}

int main(int argc, char* argv[]) {
	uint32_t bits[3];
	uint32_t bits1[3];
	cmsketch* sketch = init_sketch(64, 3);

	/* add first value with 3 hash indices */
	bits[0] = 1; // 1, 29, 22, indexes in the hashtable
	bits[1] = 29; //if you increment bits all(bits[0], bits[1], bits[2] are updated
	bits[2] = 22;

	increment_bits(sketch, bits);
	/* This should be 1 */
	expect_value(1, estimate(sketch, bits), "Test 0");

	/* add second value with different hash indices */
	bits1[0] = 29;
	bits1[1] = 21;
	bits1[2] = 2;
	increment_bits(sketch, bits1);

	expect_value(1, estimate(sketch, bits), "Test 1");
	expect_value(1, estimate(sketch, bits1), "Test 2");

	/* Add values with the same hash indexes*/
  bits1[0] = 29;
  bits1[1] = 21;
  bits1[2] = 2;
  increment_bits(sketch, bits);
  expect_value(2, estimate(sketch, bits), "Test 3");

  destroy_sketch(sketch);
  printf("You pass!\n");
	return 0;
}
