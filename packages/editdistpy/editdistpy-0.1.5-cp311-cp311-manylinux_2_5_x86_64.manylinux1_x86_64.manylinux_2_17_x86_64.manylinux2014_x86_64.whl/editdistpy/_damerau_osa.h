/**
 * MIT License
 *
 * Copyright (c) 2024 mmb L
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 */

#ifndef EDITDISTPY__DAMERAU_OSA_H_
#define EDITDISTPY__DAMERAU_OSA_H_

#include "_def.h"

#ifdef __cplusplus
extern "C" {
#endif

int Distance(const int *pString1, const int *pString2, int stringLen1,
             int stringLen2, const int64_t maxDistance);

int InternalDistance(const int *pString1, const int *pString2, const int len1,
                     const int len2, const int start);

int InternalDistanceMax(const int *pString1, const int *pString2,
                        const int len1, const int len2, const int start,
                        const int64_t maxDistance);

#ifdef __cplusplus
}
#endif

#endif // EDITDISTPY__DAMERAU_OSA_H_
