from flask import Flask, request, abort, jsonify
from skpy import Skype
import configparser

config = configparser.ConfigParser()
config.read('src/config.ini')

bitbucket_email = config.get('config', 'bitbucket_email')
bitbucket_password = config.get('config', 'bitbucket_password')
bitbucket_group = config.get('config', 'bitbucket_group')

bitbucket_sk = Skype(bitbucket_email, bitbucket_password)

bitbucket_ch = bitbucket_sk.chats[bitbucket_group]

# uptime_email = config.get('config', 'uptime_email')
# uptime_password = config.get('config', 'uptime_password')
# uptime_group = config.get('config','uptime_group')

# uptime_sk = Skype(uptime_email,
#            uptime_password)

# uptime_ch = uptime_sk.chats[uptime_group]

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health_check():
    response = jsonify({'status': 'ok'})
    return response, 200

# Commit message: test 2
# Commit hash: 6bab5d9
# Repository: bitsky
# Branch: develop

@app.route('/push', methods=['POST'])
def get_push():
    if request.method == 'POST':
        author_tuple = request.json["push"]["changes"][0]["commits"][0]["author"]["raw"],
        author = author_tuple[0].replace('(', '').replace(')', '').replace('<', '').replace('>', '')
        repo_push_status = (
                            "Author: ", author, "\n",
                            "Commit message: {message}".format(
                                message=request.json["push"]["changes"][0]["commits"][0]["message"]).rstrip("\n"), "\n",
                            "Commit hash: [{hash}]({url})".format(hash=request.json["push"]["changes"][0]["commits"][0]["hash"][:7], url=request.json["push"]["changes"][0]["new"]["target"]["links"]["html"]["href"]), "\n",
                            "Repository: [{name}]({url})".format(
                                name=request.json["repository"]["name"], url=request.json["repository"]["links"]["html"]["href"]), "\n",
                            "Branch: {branch}".format(
                                branch=request.json["push"]["changes"][0]["new"]["name"])
                            )
        
        repo_push_status_data = "".join(
            str(item) for item in repo_push_status)
        bitbucket_ch.sendMsg(repo_push_status_data, rich=True)
        return 'success', 200
    else:
        abort(400)

# Repository: bitsky
# Branch: master
# Status: SUCCESSFUL


@app.route('/build', methods=['POST'])
def get_build():
    if request.method == 'POST':
        repo_build_status = ("Repository: [{name}]({url})".format(
            name=request.json["repository"]["name"],
            url=request.json["repository"]["links"]["html"]["href"])
        ), "\n", "Branch: {name}".format(
            name=request.json["commit_status"]["refname"]
        ), "\n", "Status: [{state}]({url})".format(
            state=request.json["commit_status"]["state"],
            url=request.json["commit_status"]["url"]
        )

        repo_build_status_data = "".join(
            str(item) for item in repo_build_status)
        bitbucket_ch.sendMsg(repo_build_status_data, rich=True)
        return 'success', 200
    else:
        abort(400)

# Repository: bitsky
# Pull Request: Updating code to dazzle the algorithms
# develop 🡢 master
# Status: MERGED


@app.route('/pr', methods=['POST'])
def get_pr():
    if request.method == 'POST':
        repo_pr_status = ("Repository: [{name}]({url})".format(
            name=request.json["repository"]["name"],
            url=request.json["repository"]["links"]["html"]
            ["href"])), "\n", "Pull Request: [{name}]({url})".format(
                name=request.json["pullrequest"]["title"],
                url=request.json["pullrequest"]["links"]["html"]["href"]
        ), "\n", "{source} 🡢 {destination}".format(
                source=request.json["pullrequest"]["source"]["branch"]["name"],
                destination=request.json["pullrequest"]["destination"]
                ["branch"]["name"]), "\n", "Status: {state}".format(
                    state=request.json["pullrequest"]["state"])

        repo_pr_status_data = "".join(str(item) for item in repo_pr_status)

        bitbucket_ch.sendMsg(repo_pr_status_data, rich=True)
        return 'success', 200
    else:
        abort(400)

# @app.route('/uptime', methods=['POST'])
# def get_uptime():
#     if request.method == 'POST':

#         uptime_ch.sendMsg(request.json['msg'], rich=True)
#         return 'success', 200
#     else:
#         abort(400)


if __name__ == '__main__':
    app.run()
