if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/MasterJiraya005/Letest-Premium-Bot /Letest-Premium-Bot
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /Letest-Premium-Bot
fi
cd /Letest-Premium-Bot
pip3 install -U -r requirements.txt
echo "Bot Startingggggggggggg............."
python3 bot.py
