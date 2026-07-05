删除分支:

```python
git branch -d <分支名>

# 强制删除
git branch -D <分支名>
```

删除远程分支：

```python
git push origin --delete <分支名>
```

创建新分支并推送到远程：

```python
git checkout -b <新分支名>
# 或者用较新的
git switch -c <新分支名>

git add & commit

git push -u origin <新分支名>
```

