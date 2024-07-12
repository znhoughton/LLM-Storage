library(dplyr)
library(tidyr)
library(tidyverse)
# our sentences

df = read_csv('./Data/all_sentences.csv')

# Create a column that randomly assigns one of the sentences to group 1 or 2
df = df %>%
  group_by(Item) %>%
  mutate(group = sample(c(1, 2)))

