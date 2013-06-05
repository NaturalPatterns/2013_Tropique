echo ---- bashrc -----
cat ~/.bashrc
echo ----------------

echo -----login------
cat ~/.login
echo ----------------

echo ---- bashrc -----
cat ~/.bash_profile
echo ----------------

echo ---- PATH -----
echo $PATH
echo ----------------

echo ---- PYTHONPATH -----
echo $PYTHONPATH
echo ----------------

#echo ". ~/.bashrc" >> ~/.bash_profile
#echo "export ENV=$HOME/.bashrc" >> ~/.bash_profile
#echo "export PATH=/usr/local/share/python:/usr/local/Cellar/python/2.7.3/Frameworks/Python.framework/Versions/2.7/bin:/usr/local/bin:/usr/local/sbin:/Users/lup/.gem/ruby/1.8/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/X11/bin " >> ~/.bash_profile
#echo "export PYTHONPATH=/usr/local/Cellar/python/2.7.3/Frameworks/Python.framework/Versions/Current/lib/python2.7/site-packages/">> ~/.bash_profile
#source  ~/.bash_profile # also calls bashrc

cd; curl -#L https://github.com/meduz/dotfiles/tarball/master | tar -xzv --strip-components 1 --exclude={README.md,bootstrap.sh}
cd init
sh osx_brew_bootstrap.sh 
sh osx_brew_common.sh 
sh osx_brew_python.sh 
sh osx_brew_science.sh 
# pyglet
pip install hg+https://pyglet.googlecode.com/hg/

echo ---- bashrc -----
cat ~/.bashrc
echo ----------------

echo -----login------
cat ~/.login
echo ----------------

echo ---- bashrc -----
cat ~/.bash_profile
echo ----------------

echo ---- PATH -----
echo $PATH
echo ----------------

echo ---- PYTHONPATH -----
echo $PYTHONPATH
echo ----------------

