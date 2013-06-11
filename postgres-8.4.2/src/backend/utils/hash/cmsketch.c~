/*****************************************************************************

	 IMPORTANT: You *must* use palloc0 and pfree, not malloc and free, in your
	 implementation.  This will allow your filter to integrate into PostgreSQL.

******************************************************************************/
#include "postgres.h"
#include "utils/cmsketch.h"

/* initialize the count-min sketch for the specified width and depth */
cmsketch* init_sketch(uint32 width, uint32 depth) {
  cmsketch *sketch = palloc0(sizeof(cmsketch));
  int i;
  int j;
  sketch->table = palloc0(sizeof(uint32)*width*depth);
  for (i = 0; i < depth; i++){
    sketch->table[i]= palloc0(sizeof(uint32)*width);
  }
  sketch->width = width;
  sketch->depth = depth;
  for (i = 0; i < depth; i++){
    for(j = 0; j < width; j++){
      sketch->table[i][j] = 0;
    }
  }
  return sketch;
}

/* increment 'bits' in each sketch by 1. 
 * 'bits' is an array of indices into each row of the sketch.
 *    Thus, each index is between 0 and 'width', and there are 'depth' of them.
 */
void increment_bits(cmsketch* sketch, uint32 *bits) {
  int i;
  uint32 depth = sketch->depth;
  uint32 ** table = sketch->table;
  for(i = 0; i < depth; i++){
    int index = bits[i];
    	table[i][index]++;
  }
  sketch->table = table;
}

/* decrement 'bits' in each sketch by 1.
 * 'bits' is an array of indices into each row of the sketch.
 *    Thus, each index is between 0 and 'width', and there are 'depth' of them.
 */
void decrement_bits(cmsketch* sketch, uint32 *bits) {
  int i;
  uint32 depth = sketch->depth;
  uint32 ** table = sketch->table;
  for(i = 0; i < depth; i++){
    int index = bits[i];
    if(table[i][index] > 0){
    	table[i][index]--;
    }
  }
  sketch->table = table;
}

/* return the minimum among the indicies pointed to by 'bits'
 * 'bits' is an array of indices into each row of the sketch.
 *    Thus, each index is between 0 and 'width', and there are 'depth' of them.
 */
uint32 estimate(cmsketch* sketch, uint32 *bits) {
  uint32 min = 2147483647;
  uint32 depth = sketch->depth;
  uint32 ** table = sketch->table;
  int i;
  for (i = 0; i < depth; i++){
    int index = bits[i];
    uint32 num = table[i][index];
    if(num < min){
      min = num;
    }
  }
  return min;
}

/* set all values in the sketch to zero */
void reset_sketch(cmsketch* sketch) {
  int i;
  int j;
  uint32 depth = sketch->depth;
  uint32 width = sketch->width;
  uint32 ** table = sketch->table;
  for (i = 0; i < depth; i++){
    for(j = 0; j < width; j++){
      	table[i][j] = 0;
    }
  }
  sketch->table = table;

}

/* destroy the sketch, freeing any memory it might be using */
void destroy_sketch(cmsketch* sketch) {
  uint32 depth = sketch->depth;
  int i;
  for(i = 0; i < depth; i++){
    pfree(sketch->table[i]);
  }
  pfree(sketch->table);
  pfree(sketch);
}
