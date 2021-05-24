#ifndef FCE_H
#define FCE_H

#include "common.h"

#define FPS 60
#define W 256
#define H 240

void fce_update_screen();
void draw(int x, int y, int idx);

static const uint32_t palette[64] = {
  0x808080, 0x0000BB, 0x3700BF, 0x8400A6, 0xBB006A, 0xB7001E, 0xB30000, 0x912600,
  0x7B2B00, 0x003E00, 0x00480D, 0x003C22, 0x002F66, 0x000000, 0x050505, 0x050505,
  0xC8C8C8, 0x0059FF, 0x443CFF, 0xB733CC, 0xFF33AA, 0xFF375E, 0xFF371A, 0xD54B00,
  0xC46200, 0x3C7B00, 0x1E8415, 0x009566, 0x0084C4, 0x111111, 0x090909, 0x090909,
  0xFFFFFF, 0x0095FF, 0x6F84FF, 0xD56FFF, 0xFF77CC, 0xFF6F99, 0xFF7B59, 0xFF915F,
  0xFFA233, 0xA6BF00, 0x51D96A, 0x4DD5AE, 0x00D9FF, 0x666666, 0x0D0D0D, 0x0D0D0D,
  0xFFFFFF, 0x84BFFF, 0xBBBBFF, 0xD0BBFF, 0xFFBFEA, 0xFFBFCC, 0xFFC4B7, 0xFFCCAE,
  0xFFD9A2, 0xCCE199, 0xAEEEB7, 0xAAF7EE, 0xB3EEFF, 0xDDDDDD, 0x111111, 0x111111
};

#endif
