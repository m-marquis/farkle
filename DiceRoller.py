from cmath import inf
import numpy as np

# TODO: further strategy adjustments, plotting distributions of simulation score results 

class DiceRoller:

    def __init__(self):
        self.dice_nums = self.roll_dice(6) #np.random.randint(1, 7, 6)
        self.total_score = 0
        self.unscored_dice = self.dice_nums
        self.bank_thresh = inf
        self.score_list = []

    def roll_dice(self, n):
        return np.random.randint(1, 7, n)

    def take_turn(self):
        
        dice_nums = self.dice_nums
        self.unscored_dice = dice_nums

        # Roll until there is no more scoring
        new_score = inf
        self.total_score = 0
        while new_score > 0 and self.total_score < self.bank_thresh:
            self.unscored_dice = self.roll_dice(self.unscored_dice.size)
            tmp = self.unscored_dice
            # print('New roll: ' + str(np.sort(self.unscored_dice)))
            new_score = self.calc_score(self.unscored_dice)
            self.total_score += new_score
            # print('Scored dice: ' + str(tmp[np.invert(np.isin(tmp, self.unscored_dice))][:]))
            # print('New total score: ' + str(self.total_score))
        
        # Check to see if the rolling ended with a Farkle, bank, or hot dice
        if self.unscored_dice.size > 0 and self.total_score < self.bank_thresh:
            # Farkle
            # print('Farkle! Final score was ' + str(self.total_score))
            print('Farkle!')
            self.total_score = 0
            self.score_list.append(0)
        elif self.total_score >= self.bank_thresh:
            # Banked score
            self.score_list.append(self.total_score)
            print('Banked score of ' + str(self.total_score))
        else:
            # Hot dice - Reset dice_nums and unscored_dice but not total score
            self.dice_nums = self.roll_dice(6)
            self.unscored_dice = self.dice_nums

            # Give it one more roll for good measure
            new_score = self.calc_score(self.unscored_dice)
            if new_score > 0:
                self.total_score += new_score
                self.score_list.append(self.total_score)
                print('Hot dice! Final score is ' + str(self.total_score))
            else:
                print('Post-hot dice Farkle!')
                self.score_list.append(0)


            # print('Hot dice! Current score is ' + str(self.total_score))

    # Calculate score for a given set of dice
    def calc_score(self, dice_nums):

        dice_nums = np.asarray(dice_nums)

        unscored_dice = dice_nums.copy()

        # Return zero if input array is empty
        if dice_nums.size == 0:
            score = 0
            return score

        # Find count of each number in dice
        counts = np.asarray([(dice_nums == i).sum() for i in range(1, 7)])
        max_reps = counts.max()
        mode_val = np.argwhere(counts == max_reps) + 1  
        max_rep_num = mode_val[0][0] # Just choose first modal value in case of a tie

        # Create array containing the numbers of all the other dice
        remaining_dice = dice_nums[dice_nums != max_rep_num]

        # Calculate score
        if max_reps == 6:
            score = 3000
            self.unscored_dice = np.empty(0)
        elif max_reps == 5:
            score = 2000 + self.calc_score(remaining_dice)
        elif max_reps == 4:
            if remaining_dice.size == 2 and np.unique(remaining_dice).size == 1:  # Check if remaining dice are a pair
                score = 1500
                self.unscored_dice = np.empty(0)
            else:
                score = 1000 + self.calc_score(remaining_dice)
        elif max_reps == 3:
            if remaining_dice.size == 3 and np.unique(remaining_dice).size == 1:  # Check if remaining dice are a triplet
                score = 2500
                self.unscored_dice = np.empty(0)
            elif max_rep_num == 1:
                score = 300 + self.calc_score(remaining_dice)
            else:
                score = 100 * max_rep_num + self.calc_score(remaining_dice)
        elif max_reps == 2:
            if remaining_dice.size == 4 and np.unique(remaining_dice).size == 2:  # Check if remaining dice are two pairs
                score = 1500
                self.unscored_dice = np.empty(0)
            else:
                num_ones = (dice_nums == 1).sum()
                num_fives = (dice_nums == 5).sum()
                score = 50*num_fives + 100*num_ones
                unscored_dice = dice_nums[np.all([dice_nums != 1, dice_nums !=5], axis=0)]
                if unscored_dice.size > 0:
                    self.unscored_dice = unscored_dice
                else:
                    self.unscored_dice = np.empty(0)
        else:
            if dice_nums.size == 6:    
                score = 1500
                self.unscored_dice = np.empty(0)
            else:
                num_ones = (dice_nums == 1).sum()
                num_fives = (dice_nums == 5).sum()
                score = 50*num_fives + 100*num_ones
                unscored_dice = dice_nums[np.all([dice_nums != 1, dice_nums !=5], axis=0)]
                if unscored_dice.size > 0:
                    self.unscored_dice = unscored_dice
                else:
                    self.unscored_dice = np.empty(0)
                    
        return score


test = DiceRoller()
test.bank_thresh = 250
# print('Starting score: ' + str(test.total_score))
# # test.dice_nums = np.asarray([5, 1, 1, 6, 6, 3])
# test.take_turn()
# # print('Starting dice roll: ' + str(test.dice_nums))
# print('Final score: ' + str(test.total_score))

mean_scores = []
test_thresholds = [150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500] 
for i in test_thresholds:
    test = DiceRoller()
    test.bank_thresh = i
    for j in range(200000):
        test.take_turn()
    mean_scores.append(np.mean(test.score_list))

for i, j in zip(test_thresholds, mean_scores):
    print('Thresh ' + str(i) + ' mean score: ' + str(j))