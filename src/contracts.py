from pyteal import *

var_author = Bytes("author")


def blog_program():
    # Code block invoked during contract initialization. Sets the
    # author to be the sender (creator) of this smart contract
    init_contract = Seq([
        App.globalPut(var_author, Txn.sender()),
        Return(Int(1))
    ])

    # Checks if the sender of the current transaction invoking this
    # smart contract is the current author
    is_author = Txn.sender() == App.globalGet(var_author)


    # Code block invoked during blog issuance. Only the author
    # may invoke this block with two arguments and one account supplied.
    # The first argument was "issue_blog" used by the control flow
    # below. The second argument is the blog metadata which is
    # set to the local storage of the supplied account (Int(1))
    blog_metadata = Txn.application_args[1]
    issue_blog = Seq([
        Assert(is_author),
        Assert(Txn.application_args.length() == Int(2)),
        App.localPut(Int(1), Bytes('blog'), blog_metadata),
        Return(Int(1))
    ])

    # Code block invoked during blog revocation. Only the author
    # may invoke this block with one argument and one account supplied.
    # The first argument was "revoke_blog" used by the control flow
    # below. The local storage containing the blog metadata of the
    # supplied account (Int(1)) is deleted.
    revoke_blog = Seq([
        Assert(is_author),
        Assert(Txn.application_args.length() == Int(1)),
        App.localDel(Int(1), Bytes('blog')),
        Return(Int(1))
    ])

    program = Cond(
        [Txn.application_id() == Int(0), init_contract],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(is_author)],
        [Txn.on_completion() == OnComplete.UpdateApplication, Return(is_author)],
        [Txn.on_completion() == OnComplete.OptIn, Return(Int(1))],
        [Txn.on_completion() == OnComplete.CloseOut, Return(Int(1))],
        [Txn.application_args[0] == Bytes("issue_blog"), issue_blog],
        [Txn.application_args[0] == Bytes("revoke_blog"), revoke_blog]
    )

    return program


if __name__ == "__main__":
    print(compileTeal(blog_program(), Mode.Application, version=3))
