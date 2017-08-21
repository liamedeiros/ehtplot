gh-pages:
	@if [ -n "`git status -s`" ]; then \
		echo "Work directory is not clean; please commit before creating the GitHub page."; \
		exit 1; \
	fi

	@if git rev-parse --quiet --verify gh-pages; then \
		git branch -D gh-pages; \
	fi

	pushd doc && ln -s .. html; doxygen; rm html; popd
	git checkout --orphan gh-pages && git rm -rf . && git add . && git commit -m 'GitHub Page'
	git checkout master
	git push --force origin gh-pages
