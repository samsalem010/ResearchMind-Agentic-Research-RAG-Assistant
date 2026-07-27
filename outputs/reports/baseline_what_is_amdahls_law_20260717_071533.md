# Research Report: Baseline_What Is Amdahls Law 

**Generated on:** 2026-07-17 07:15:33

---

Amdahl's Law is a fundamental principle in computer science that describes the maximum theoretical speedup that can be achieved by parallel processing. It was first proposed by Gene Amdahl in 1967 and is a key concept in understanding the limitations of parallel computing.

**Definition:**

Amdahl's Law states that the maximum theoretical speedup that can be achieved by parallel processing is limited by the fraction of the program that cannot be parallelized. In other words, the law states that the speedup of a program using multiple processors is limited by the portion of the program that must be executed sequentially.

**Mathematical Formula:**

The law can be expressed mathematically as follows:

S = 1 / (1 - P + P/N)

where:
S = maximum theoretical speedup
P = fraction of the program that can be parallelized
N = number of processors

**Interpretation:**

The law implies that as the number of processors (N) increases, the speedup (S) approaches a limit that is determined by the fraction of the program that cannot be parallelized (1-P). This means that even with an infinite number of processors, the speedup will be limited by the sequential portion of the program.

**Example:**

Suppose we have a program that consists of 90% parallelizable code and 10% sequential code. If we run this program on a single processor, the execution time is 100 seconds. If we run it on 10 processors, the parallelizable portion of the code will be executed 10 times faster, but the sequential portion will still take 10 seconds. Therefore, the total execution time will be approximately 19 seconds (10 seconds for the sequential portion + 9 seconds for the parallelizable portion). In this case, the speedup is approximately 5.26 (100/19).

However, if we increase the number of processors to 100, the parallelizable portion will be executed 100 times faster, but the sequential portion will still take 10 seconds. Therefore, the total execution time will be approximately 10.1 seconds (10 seconds for the sequential portion + 0.1 seconds for the parallelizable portion). In this case, the speedup is approximately 9.9 (100/10.1).

**Implications:**

Amdahl's Law has several implications for parallel computing:

1. **Limitations of parallel processing**: The law highlights the limitations of parallel processing in achieving speedup. Even with an infinite number of processors, the speedup will be limited by the sequential portion of the program.
2. **Importance of parallelizable code**: The law emphasizes the importance of writing parallelizable code to achieve significant speedup.
3. **Optimizing sequential code**: The law suggests that optimizing the sequential portion of the code can lead to significant improvements in overall performance.

In summary, Amdahl's Law provides a theoretical framework for understanding the limitations of parallel processing and highlights the importance of writing parallelizable code and optimizing sequential code to achieve significant speedup.
