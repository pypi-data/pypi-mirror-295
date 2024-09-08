// THIS FILE IS AUTO-GENERATED. You can regenerate it by running `go generate ./...` at the root of the lazygit repo.

package tests

import (
	"github.com/jesseduffield/lazygit/pkg/integration/components"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/bisect"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/branch"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/cherry_pick"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/commit"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/config"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/conflicts"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/custom_commands"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/demo"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/diff"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/file"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/filter_and_search"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/filter_by_author"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/filter_by_path"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/interactive_rebase"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/misc"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/patch_building"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/reflog"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/shell_commands"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/staging"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/stash"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/status"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/submodule"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/sync"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/tag"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/ui"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/undo"
	"github.com/jesseduffield/lazygit/pkg/integration/tests/worktree"
)

var tests = []*components.IntegrationTest{
	bisect.Basic,
	bisect.ChooseTerms,
	bisect.FromOtherBranch,
	bisect.Skip,
	branch.CheckoutAutostash,
	branch.CheckoutByName,
	branch.CreateTag,
	branch.Delete,
	branch.DeleteRemoteBranchWithCredentialPrompt,
	branch.DetachedHead,
	branch.NewBranchAutostash,
	branch.NewBranchFromRemoteTrackingDifferentName,
	branch.NewBranchFromRemoteTrackingSameName,
	branch.OpenPullRequestNoUpstream,
	branch.OpenWithCliArg,
	branch.Rebase,
	branch.RebaseAbortOnConflict,
	branch.RebaseAndDrop,
	branch.RebaseCancelOnConflict,
	branch.RebaseConflictsFixBuildErrors,
	branch.RebaseCopiedBranch,
	branch.RebaseDoesNotAutosquash,
	branch.RebaseFromMarkedBase,
	branch.RebaseOntoBaseBranch,
	branch.RebaseToUpstream,
	branch.Rename,
	branch.Reset,
	branch.ResetToUpstream,
	branch.SetUpstream,
	branch.ShowDivergenceFromBaseBranch,
	branch.ShowDivergenceFromUpstream,
	branch.SortLocalBranches,
	branch.SortRemoteBranches,
	branch.SquashMerge,
	branch.Suggestions,
	branch.UnsetUpstream,
	cherry_pick.CherryPick,
	cherry_pick.CherryPickConflicts,
	cherry_pick.CherryPickDuringRebase,
	cherry_pick.CherryPickRange,
	commit.AddCoAuthor,
	commit.AddCoAuthorRange,
	commit.AddCoAuthorWhileCommitting,
	commit.Amend,
	commit.AutoWrapMessage,
	commit.Commit,
	commit.CommitMultiline,
	commit.CommitSwitchToEditor,
	commit.CommitWipWithPrefix,
	commit.CommitWithGlobalPrefix,
	commit.CommitWithNonMatchingBranchName,
	commit.CommitWithPrefix,
	commit.CreateAmendCommit,
	commit.CreateTag,
	commit.DiscardOldFileChanges,
	commit.FindBaseCommitForFixup,
	commit.FindBaseCommitForFixupDisregardMainBranch,
	commit.FindBaseCommitForFixupOnlyAddedLines,
	commit.FindBaseCommitForFixupWarningForAddedLines,
	commit.Highlight,
	commit.History,
	commit.HistoryComplex,
	commit.NewBranch,
	commit.NewBranchWithPrefix,
	commit.PasteCommitMessage,
	commit.PasteCommitMessageOverExisting,
	commit.PreserveCommitMessage,
	commit.ResetAuthor,
	commit.ResetAuthorRange,
	commit.Revert,
	commit.RevertMerge,
	commit.Reword,
	commit.Search,
	commit.SetAuthor,
	commit.SetAuthorRange,
	commit.StageRangeOfLines,
	commit.Staged,
	commit.StagedWithoutHooks,
	commit.Unstaged,
	config.CustomCommandsInPerRepoConfig,
	config.RemoteNamedStar,
	conflicts.Filter,
	conflicts.ResolveExternally,
	conflicts.ResolveMultipleFiles,
	conflicts.ResolveNoAutoStage,
	conflicts.UndoChooseHunk,
	custom_commands.AccessCommitProperties,
	custom_commands.BasicCommand,
	custom_commands.CheckForConflicts,
	custom_commands.FormPrompts,
	custom_commands.GlobalContext,
	custom_commands.MenuFromCommand,
	custom_commands.MenuFromCommandsOutput,
	custom_commands.MultipleContexts,
	custom_commands.MultiplePrompts,
	custom_commands.SelectedCommit,
	custom_commands.SelectedPath,
	custom_commands.ShowOutputInPanel,
	custom_commands.SuggestionsCommand,
	custom_commands.SuggestionsPreset,
	demo.AmendOldCommit,
	demo.Bisect,
	demo.CherryPick,
	demo.CommitAndPush,
	demo.CommitGraph,
	demo.CustomCommand,
	demo.CustomPatch,
	demo.DiffCommits,
	demo.Filter,
	demo.InteractiveRebase,
	demo.NukeWorkingTree,
	demo.RebaseOnto,
	demo.StageLines,
	demo.Undo,
	demo.WorktreeCreateFromBranches,
	diff.Diff,
	diff.DiffAndApplyPatch,
	diff.DiffCommits,
	diff.DiffNonStickyRange,
	diff.IgnoreWhitespace,
	diff.RenameSimilarityThresholdChange,
	file.CopyMenu,
	file.DirWithUntrackedFile,
	file.DiscardAllDirChanges,
	file.DiscardRangeSelect,
	file.DiscardStagedChanges,
	file.DiscardUnstagedDirChanges,
	file.DiscardUnstagedFileChanges,
	file.DiscardUnstagedRangeSelect,
	file.DiscardVariousChanges,
	file.DiscardVariousChangesRangeSelect,
	file.Gitignore,
	file.RememberCommitMessageAfterFail,
	file.RenameSimilarityThresholdChange,
	file.StageChildrenRangeSelect,
	file.StageDeletedRangeSelect,
	file.StageRangeSelect,
	filter_and_search.FilterCommitFiles,
	filter_and_search.FilterFiles,
	filter_and_search.FilterFuzzy,
	filter_and_search.FilterMenu,
	filter_and_search.FilterMenuCancelFilterWithEscape,
	filter_and_search.FilterMenuWithNoKeybindings,
	filter_and_search.FilterRemoteBranches,
	filter_and_search.FilterRemotes,
	filter_and_search.FilterSearchHistory,
	filter_and_search.FilterUpdatesWhenModelChanges,
	filter_and_search.NestedFilter,
	filter_and_search.NestedFilterTransient,
	filter_and_search.NewSearch,
	filter_by_author.SelectAuthor,
	filter_by_author.TypeAuthor,
	filter_by_path.CliArg,
	filter_by_path.KeepSameCommitSelectedOnExit,
	filter_by_path.SelectFile,
	filter_by_path.TypeFile,
	interactive_rebase.AdvancedInteractiveRebase,
	interactive_rebase.AmendCommitWithConflict,
	interactive_rebase.AmendFirstCommit,
	interactive_rebase.AmendFixupCommit,
	interactive_rebase.AmendHeadCommitDuringRebase,
	interactive_rebase.AmendMerge,
	interactive_rebase.AmendNonHeadCommitDuringRebase,
	interactive_rebase.DeleteUpdateRefTodo,
	interactive_rebase.DontShowBranchHeadsForTodoItems,
	interactive_rebase.DropCommitInCopiedBranchWithUpdateRef,
	interactive_rebase.DropTodoCommitWithUpdateRef,
	interactive_rebase.DropWithCustomCommentChar,
	interactive_rebase.EditFirstCommit,
	interactive_rebase.EditNonTodoCommitDuringRebase,
	interactive_rebase.EditRangeSelectOutsideRebase,
	interactive_rebase.EditTheConflCommit,
	interactive_rebase.FixupFirstCommit,
	interactive_rebase.FixupSecondCommit,
	interactive_rebase.InteractiveRebaseOfCopiedBranch,
	interactive_rebase.MidRebaseRangeSelect,
	interactive_rebase.Move,
	interactive_rebase.MoveInRebase,
	interactive_rebase.MoveUpdateRefTodo,
	interactive_rebase.MoveWithCustomCommentChar,
	interactive_rebase.OutsideRebaseRangeSelect,
	interactive_rebase.PickRescheduled,
	interactive_rebase.QuickStart,
	interactive_rebase.QuickStartKeepSelection,
	interactive_rebase.QuickStartKeepSelectionRange,
	interactive_rebase.Rebase,
	interactive_rebase.RewordCommitWithEditorAndFail,
	interactive_rebase.RewordFirstCommit,
	interactive_rebase.RewordLastCommit,
	interactive_rebase.RewordYouAreHereCommit,
	interactive_rebase.RewordYouAreHereCommitWithEditor,
	interactive_rebase.ShowExecTodos,
	interactive_rebase.SquashDownFirstCommit,
	interactive_rebase.SquashDownSecondCommit,
	interactive_rebase.SquashFixupsAbove,
	interactive_rebase.SquashFixupsAboveFirstCommit,
	interactive_rebase.SquashFixupsInCurrentBranch,
	interactive_rebase.SwapInRebaseWithConflict,
	interactive_rebase.SwapInRebaseWithConflictAndEdit,
	interactive_rebase.SwapWithConflict,
	interactive_rebase.ViewFilesOfTodoEntries,
	misc.ConfirmOnQuit,
	misc.CopyToClipboard,
	misc.DisabledKeybindings,
	misc.InitialOpen,
	misc.RecentReposOnLaunch,
	patch_building.Apply,
	patch_building.ApplyInReverse,
	patch_building.ApplyInReverseWithConflict,
	patch_building.MoveRangeToIndex,
	patch_building.MoveToEarlierCommit,
	patch_building.MoveToEarlierCommitFromAddedFile,
	patch_building.MoveToEarlierCommitNoKeepEmpty,
	patch_building.MoveToIndex,
	patch_building.MoveToIndexFromAddedFileWithConflict,
	patch_building.MoveToIndexPartOfAdjacentAddedLines,
	patch_building.MoveToIndexPartial,
	patch_building.MoveToIndexWithConflict,
	patch_building.MoveToIndexWorksEvenIfNoprefixIsSet,
	patch_building.MoveToLaterCommit,
	patch_building.MoveToLaterCommitPartialHunk,
	patch_building.MoveToNewCommit,
	patch_building.MoveToNewCommitFromAddedFile,
	patch_building.MoveToNewCommitFromDeletedFile,
	patch_building.MoveToNewCommitPartialHunk,
	patch_building.RemoveFromCommit,
	patch_building.RemovePartsOfAddedFile,
	patch_building.ResetWithEscape,
	patch_building.SelectAllFiles,
	patch_building.SpecificSelection,
	patch_building.StartNewPatch,
	patch_building.ToggleRange,
	reflog.Checkout,
	reflog.CherryPick,
	reflog.DoNotShowBranchMarkersInReflogSubcommits,
	reflog.Patch,
	reflog.Reset,
	shell_commands.BasicShellCommand,
	shell_commands.ComplexShellCommand,
	shell_commands.DeleteFromHistory,
	shell_commands.EditHistory,
	shell_commands.History,
	shell_commands.OmitFromHistory,
	staging.DiffChangeScreenMode,
	staging.DiffContextChange,
	staging.DiscardAllChanges,
	staging.Search,
	staging.StageHunks,
	staging.StageLines,
	staging.StageRanges,
	stash.Apply,
	stash.ApplyPatch,
	stash.CreateBranch,
	stash.Drop,
	stash.Pop,
	stash.PreventDiscardingFileChanges,
	stash.Rename,
	stash.Stash,
	stash.StashAll,
	stash.StashAndKeepIndex,
	stash.StashIncludingUntrackedFiles,
	stash.StashStaged,
	stash.StashStagedPartialFile,
	stash.StashUnstaged,
	status.ClickRepoNameToOpenReposMenu,
	status.ClickToFocus,
	status.ClickWorkingTreeStateToOpenRebaseOptionsMenu,
	status.LogCmd,
	status.ShowDivergenceFromBaseBranch,
	submodule.Add,
	submodule.Enter,
	submodule.EnterNested,
	submodule.Remove,
	submodule.RemoveNested,
	submodule.Reset,
	sync.FetchPrune,
	sync.FetchWhenSortedByDate,
	sync.ForcePush,
	sync.ForcePushMultipleMatching,
	sync.ForcePushMultipleUpstream,
	sync.ForcePushRemoteBranchNotStoredLocally,
	sync.ForcePushTriangular,
	sync.Pull,
	sync.PullAndSetUpstream,
	sync.PullMerge,
	sync.PullMergeConflict,
	sync.PullRebase,
	sync.PullRebaseConflict,
	sync.PullRebaseInteractiveConflict,
	sync.PullRebaseInteractiveConflictDrop,
	sync.Push,
	sync.PushAndAutoSetUpstream,
	sync.PushAndSetUpstream,
	sync.PushFollowTags,
	sync.PushNoFollowTags,
	sync.PushTag,
	sync.PushWithCredentialPrompt,
	sync.RenameBranchAndPull,
	tag.Checkout,
	tag.CheckoutWhenBranchWithSameNameExists,
	tag.CreateWhileCommitting,
	tag.CrudAnnotated,
	tag.CrudLightweight,
	tag.ForceTagAnnotated,
	tag.ForceTagLightweight,
	tag.Reset,
	ui.Accordion,
	ui.DoublePopup,
	ui.EmptyMenu,
	ui.KeybindingSuggestionsWhenSwitchingRepos,
	ui.ModeSpecificKeybindingSuggestions,
	ui.OpenLinkFailure,
	ui.RangeSelect,
	ui.SwitchTabFromMenu,
	ui.SwitchTabWithPanelJumpKeys,
	undo.UndoCheckoutAndDrop,
	undo.UndoDrop,
	worktree.AddFromBranch,
	worktree.AddFromBranchDetached,
	worktree.AddFromCommit,
	worktree.AssociateBranchBisect,
	worktree.AssociateBranchRebase,
	worktree.BareRepo,
	worktree.BareRepoWorktreeConfig,
	worktree.Crud,
	worktree.CustomCommand,
	worktree.DetachWorktreeFromBranch,
	worktree.DotfileBareRepo,
	worktree.DoubleNestedLinkedSubmodule,
	worktree.ExcludeFileInWorktree,
	worktree.FastForwardWorktreeBranch,
	worktree.ForceRemoveWorktree,
	worktree.RemoveWorktreeFromBranch,
	worktree.ResetWindowTabs,
	worktree.SymlinkIntoRepoSubdir,
	worktree.WorktreeInRepo,
}
