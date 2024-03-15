This project is not complete yet.

To check functionality, run app.py.

There are two models: one for recognizing hero icons on a screenshot and second for predicting which side (Radiant or Dire) wins. Both models still make mistakes, so I am constantly extending the datasets.

For now, first model can predict heroes only from the game itself (take a screenshot when drafts finished), you can see that from edit_image.py. I will add more options later.

I will also add more features for second model to improve precisions, as 200k lines of match data on which model was trained on is not enough. I am currently searching for them (check hero_data lists).

P.S. Model for recognizing hero icons is too large, so here is download link: https://drive.google.com/file/d/1vBA3p5u-w8NrDZ_vuhAUZzNJyKncARnW/view?usp=drive_link. In other case, you can train yourself by running train_image_predictor.py.
P.S.S This is my first relatively serious project.
