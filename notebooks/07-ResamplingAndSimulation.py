# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Resampling and simulation in R
#
# ## Generating random samples
# Here we will generate random samples from a number of different distributions and plot their histograms.

# %%


# ```{r fig.height=8, fig.width=8}

# nsamples <- 10000
# nhistbins <- 100

# # uniform distribution

# p1 <-
#   tibble(
#     x = runif(nsamples)
#   ) %>% 
#   ggplot((aes(x))) +
#   geom_histogram(bins = nhistbins) + 
#   labs(title = "Uniform")

# # normal distribution
# p2 <-
#   tibble(
#     x = rnorm(nsamples)
#   ) %>% 
#   ggplot(aes(x)) +
#   geom_histogram(bins = nhistbins) +
#   labs(title = "Normal")

# # Chi-squared distribution
# p3 <-
#   tibble(
#     x = rnorm(nsamples)
#   ) %>% 
#   ggplot(aes(x)) +
#   geom_histogram(bins = nhistbins) +
#   labs(title = "Normal")

# # Chi-squared distribution
# p3 <-
#   tibble(
#     x = rchisq(nsamples, df=1)
#   ) %>% 
#   ggplot(aes(x)) +
#   geom_histogram(bins = nhistbins) +
#   labs(title = "Chi-squared")

# # Poisson distribution
# p4 <-
#   tibble(
#     x = rbinom(nsamples, 20, 0.25)
#   ) %>% 
#   ggplot(aes(x)) +
#   geom_histogram(bins = nhistbins) +
#   labs(title = "Binomial (p=0.25, 20 trials)")


# plot_grid(p1, p2, p3, p4, ncol = 2)

# ```

# ## Simulating the maximum finishing time

# Let's simulate 150 samples, collecting the maximum value from each sample, and then plotting the distribution of maxima.

# ```{r fig.width=4, fig.height=4, out.width="50%"}
# # sample maximum value 5000 times and compute 99th percentile
# nRuns <- 5000
# sampSize <- 150

# sampleMax <- function(sampSize = 150) {
#   samp <- rnorm(sampSize, mean = 5, sd = 1)
#   return(tibble(max=max(samp)))
# }

# input_df <- tibble(id=seq(nRuns)) %>%
#   group_by(id)

# maxTime <- input_df %>% do(sampleMax())

# cutoff <- quantile(maxTime$max, 0.99)


# ggplot(maxTime,aes(max)) +
#   geom_histogram(bins = 100) +
#   geom_vline(xintercept = cutoff, color = "red")

# ```

# ## The bootstrap

# The bootstrap is useful for creating confidence intervals in cases where we don't have a parametric distribution. One example is for the median; let's look at how that works. We will start by implementing it by hand, to see more closely how it works.  We will start by collecting a sample of individuals from the NHANES dataset, and the using the bootstrap to obtain confidence intervals on the median for the Height variable.

# ```{r echo=FALSE}

# nRuns <- 2500
# sampleSize <- 64

# # take a sample
# heightSample <- 
#   NHANES_adult %>%
#   sample_n(sampleSize)

# # create a function to collect a sample with replacement
# bootMedianHeight <- function(df) {
#   bootSample <- sample_n(df, dim(df)[1], replace = TRUE)
#   return(tibble(medianHeight=median(bootSample$Height)))
# }

# input_df <- tibble(id=seq(nRuns)) %>%
#   group_by(id)

# bootMeans <- do(input_df, bootMedianHeight(heightSample))

# bootCI <- tibble(`Lower CI limit`=quantile(bootMeans$medianHeight,.025),
#             Median=median(heightSample$Height),
#             `Upper CI limit`=quantile(bootMeans$medianHeight,.975)
#             )
# kable(bootCI)
# ```

