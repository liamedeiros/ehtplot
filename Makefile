gh-pages:
	if [ `git rev-parse --verify gh-pages 2> /dev/null` ]; then git branch -D gh-pages; fi
	pushd doc && ln -s .. html; doxygen; rm html; popd
	git checkout --orphan gh-pages && git rm -rf . && git add . && git commit -m 'GitHub Page'
	git checkout master
