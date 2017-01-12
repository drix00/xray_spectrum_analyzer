/**
 * @file
 *
 * @brief Test the dlib library for fitting.
 *
 * @author Hendrix Demers <hendrix.demers@mail.mcgill.ca>
 * @since 1.0
 */

// Copyright 2016 Hendrix Demers
//
//   Licensed under the Apache License, Version 2.0 (the "License");
//   you may not use this file except in compliance with the License.
//   You may obtain a copy of the License at
//
//       http://www.apache.org/licenses/LICENSE-2.0
//
//   Unless required by applicable law or agreed to in writing, software
//   distributed under the License is distributed on an "AS IS" BASIS,
//   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//   See the License for the specific language governing permissions and
//   limitations under the License.

// C system headers
// C++ system header
#include <iostream>
#include <vector>
// Library headers
#include <boost/test/unit_test.hpp>
#include <boost/test/floating_point_comparison.hpp>
// Precompiled header
#pragma hdrstop
// Current declaration header file of this implementation file.
#include <dlib/optimization.h>
// Project headers
// Project private headers

// Global and constant variables/functions.

using namespace std;
using namespace dlib;

typedef matrix<double,2,1> input_vector;
typedef matrix<double,3,1> parameter_vector;

// We will use this function to generate data.  It represents a function of 2 variables
// and 3 parameters.   The least squares procedure will be used to infer the values of
// the 3 parameters based on a set of input/output pairs.
double model (
        const input_vector& input,
        const parameter_vector& params
)
{
    const double p0 = params(0);
    const double p1 = params(1);
    const double p2 = params(2);

    const double i0 = input(0);
    const double i1 = input(1);

    const double temp = p0*i0 + p1*i1 + p2;

    return temp*temp;
}

// ----------------------------------------------------------------------------------------

// This function is the "residual" for a least squares problem.   It takes an input/output
// pair and compares it to the output of our model and returns the amount of error.  The idea
// is to find the set of parameters which makes the residual small on all the data pairs.
double residual (
        const std::pair<input_vector, double>& data,
        const parameter_vector& params
)
{
    return model(data.first, params) - data.second;
}

// ----------------------------------------------------------------------------------------

// This function is the derivative of the residual() function with respect to the parameters.
parameter_vector residual_derivative (
        const std::pair<input_vector, double>& data,
        const parameter_vector& params
)
{
    parameter_vector der;

    const double p0 = params(0);
    const double p1 = params(1);
    const double p2 = params(2);

    const double i0 = data.first(0);
    const double i1 = data.first(1);

    const double temp = p0*i0 + p1*i1 + p2;

    der(0) = i0*2*temp;
    der(1) = i1*2*temp;
    der(2) = 2*temp;

    return der;
}

BOOST_AUTO_TEST_SUITE(test_dlib)

/**
 * @brief Test if this testcase file is included in the testsuite and run.
 */
BOOST_AUTO_TEST_CASE(test_is_working)
{
    //BOOST_FAIL( "Nothing to test" );
    BOOST_CHECK(true);
}

    /**
     * @brief Test
     */
    BOOST_AUTO_TEST_CASE(test_least_square_example)
    {
        const double tolerance = 0.001;

        try
        {
            // randomly pick a set of parameters to use in this example
            const parameter_vector params = 10*randm(3,1);

            // Now let's generate a bunch of input/output pairs according to our model.
            std::vector<std::pair<input_vector, double> > data_samples;
            input_vector input;
            for (int i = 0; i < 1000; ++i)
            {
                input = 10*randm(2,1);
                const double output = model(input, params);

                // save the pair
                data_samples.push_back(make_pair(input, output));
            }

            // Before we do anything, let's make sure that our derivative function defined above matches
            // the approximate derivative computed using central differences (via derivative()).
            // If this value is big then it means we probably typed the derivative function incorrectly.
            BOOST_CHECK_SMALL(length(residual_derivative(data_samples[0], params) -
                                                  derivative(residual)(data_samples[0], params) ), 1.0e-05);

            // Now let's use the solve_least_squares_lm() routine to figure out what the
            // parameters are based on just the data_samples.
            parameter_vector x;

            x = 1;
            // Use the Levenberg-Marquardt method to determine the parameters which
            // minimize the sum of all squared residuals.
            solve_least_squares_lm(objective_delta_stop_strategy(1e-7),
                                   residual,
                                   residual_derivative,
                                   data_samples,
                                   x);

            // Now x contains the solution.  If everything worked it will be equal to params.
            BOOST_CHECK_CLOSE(params(0, 0), x(0, 0), tolerance);
            BOOST_CHECK_CLOSE(params(1, 0), x(1, 0), tolerance);
            BOOST_CHECK_CLOSE(params(2, 0), x(2, 0), tolerance);
            BOOST_CHECK_SMALL(length(x - params), 3.0e-15);

            x = 1;
            // Use the Levenberg-Marquardt method to determine the parameters which
            // minimize the sum of all squared residuals.
            solve_least_squares_lm(objective_delta_stop_strategy(1e-7),
                                   residual,
                                   derivative(residual),
                                   data_samples,
                                   x);

            // Now x contains the solution.  If everything worked it will be equal to params.
            BOOST_CHECK_CLOSE(params(0, 0), x(0, 0), tolerance);
            BOOST_CHECK_CLOSE(params(1, 0), x(1, 0), tolerance);
            BOOST_CHECK_CLOSE(params(2, 0), x(2, 0), tolerance);
            BOOST_CHECK_SMALL(length(x - params), 5.0e-15);

            x = 1;
            // If we didn't create the residual_derivative function then we could
            // have used this method which numerically approximates the derivatives for you.
            solve_least_squares_lm(objective_delta_stop_strategy(1e-7),
                                   residual,
                                   derivative(residual),
                                   data_samples,
                                   x);

            // Now x contains the solution.  If everything worked it will be equal to params.
            BOOST_CHECK_CLOSE(params(0, 0), x(0, 0), tolerance);
            BOOST_CHECK_CLOSE(params(1, 0), x(1, 0), tolerance);
            BOOST_CHECK_CLOSE(params(2, 0), x(2, 0), tolerance);
            BOOST_CHECK_SMALL(length(x - params), 1.0e-14);

            x = 1;
            // This version of the solver uses a method which is appropriate for problems
            // where the residuals don't go to zero at the solution.  So in these cases
            // it may provide a better answer.
            solve_least_squares(objective_delta_stop_strategy(1e-7),
                                residual,
                                residual_derivative,
                                data_samples,
                                x);

            // Now x contains the solution.  If everything worked it will be equal to params.
            BOOST_CHECK_CLOSE(params(0, 0), x(0, 0), tolerance);
            BOOST_CHECK_CLOSE(params(1, 0), x(1, 0), tolerance);
            BOOST_CHECK_CLOSE(params(2, 0), x(2, 0), tolerance);
            BOOST_CHECK_SMALL(length(x - params), 1.0e-14);
        }
        catch (std::exception& e)
        {
            cout << e.what() << endl;
        }

        //BOOST_FAIL( "Nothing to test" );
        BOOST_CHECK(true);
    }

BOOST_AUTO_TEST_SUITE_END()
