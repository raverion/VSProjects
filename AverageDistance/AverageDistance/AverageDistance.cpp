#include <iostream>

unsigned long long  factorial(int n)
{
	if (n == 0)
		return 1;
	else
		return n * factorial(n - 1);
}

unsigned long long nCr(int n, int r)
{
	unsigned long long i = factorial(n);
	unsigned long long j = factorial(n-r);
	unsigned long long k = factorial(r);
	return factorial(n) / (factorial(n - r) * factorial(r));
}

int average_distance(int num_points)
{

	int num_divs = num_points - 1;

	unsigned long long  num_pairs = nCr(num_points, 2);

	double div = 1 / num_divs;

	double sum_of_all_distances = 0;

	int i = 0, z = 0;
	for (int z = num_divs-i; z > 0; i++)
		sum_of_all_distances = sum_of_all_distances + div * (i + 1) * (num_divs - i);

	return sum_of_all_distances / num_pairs;

}

int main()
{
	double avg = average_distance(1000);
	std::cout << avg << std::endl;
}