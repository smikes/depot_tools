  is_new = False
  def get(self):  # pragma: no coverage
  def __init__(self, filename, data, svn_properties, is_new):
    self.is_new = is_new
    last_line = ''

      # TODO(maruel): old should be replace with self.source_file
      # TODO(maruel): new == self.filename and remove new
      self._verify_git_header_process_line(lines, line, last_line, old, new)
      last_line = line
    # Cheap check to make sure the file name is at least mentioned in the
    # 'diff' header. That the only remaining invariant.
    if not self.filename in self.diff_header:
      self._fail('Diff seems corrupted.')
  def _verify_git_header_process_line(self, lines, line, last_line, old, new):
    """Processes a single line of the header.

    Returns True if it should continue looping.

    Format is described to
    http://www.kernel.org/pub/software/scm/git/docs/git-diff.html
    """
    match = re.match(r'^(rename|copy) from (.+)$', line)
    if match:
      if old != match.group(2):
        self._fail('Unexpected git diff input name for line %s.' % line)
      if not lines or not lines[0].startswith('%s to ' % match.group(1)):
        self._fail(
            'Confused %s from/to git diff for line %s.' %
                (match.group(1), line))
      return

    match = re.match(r'^(rename|copy) to (.+)$', line)
    if match:
      if new != match.group(2):
        self._fail('Unexpected git diff output name for line %s.' % line)
      if not last_line.startswith('%s from ' % match.group(1)):
        self._fail(
            'Confused %s from/to git diff for line %s.' %
                (match.group(1), line))
      return

    match = re.match(r'^new(| file) mode (\d{6})$', line)
    if match:
      mode = match.group(2)
      # Only look at owner ACL for executable.
      # TODO(maruel): Add support to remove a property.
      if bool(int(mode[4]) & 1):
        self.svn_properties.append(('svn:executable', '*'))

    match = re.match(r'^--- (.*)$', line)
    if match:
      if last_line[:3] in ('---', '+++'):
        self._fail('--- and +++ are reversed')
      self.is_new = match.group(1) == '/dev/null'
      # TODO(maruel): Use self.source_file.
      if not lines or not lines[0].startswith('+++'):
      return

    match = re.match(r'^\+\+\+ (.*)$', line)
    if match:
      if not last_line.startswith('---'):
      # TODO(maruel): new == self.filename.
        # TODO(maruel): Can +++ be /dev/null? If so, assert self.is_delete ==
        # True.
      if lines:
        self._fail('Crap after +++')
      # We're done.
      return
    last_line = ''

      line = lines.pop(0)
      self._verify_svn_header_process_line(lines, line, last_line)
      last_line = line

    # Cheap check to make sure the file name is at least mentioned in the
    # 'diff' header. That the only remaining invariant.
    if not self.filename in self.diff_header:
      self._fail('Diff seems corrupted.')

  def _verify_svn_header_process_line(self, lines, line, last_line):
    """Processes a single line of the header.

    Returns True if it should continue looping.
    """
    match = re.match(r'^--- ([^\t]+).*$', line)
    if match:
      if last_line[:3] in ('---', '+++'):
        self._fail('--- and +++ are reversed')
      self.is_new = match.group(1) == '/dev/null'
      # For copy and renames, it's possible that the -- line doesn't match
      # +++, so don't check match.group(1) to match self.filename or
      # '/dev/null', it can be anything else.
      # if (self.mangle(match.group(1)) != self.filename and
      #     match.group(1) != '/dev/null'):
      if not lines or not lines[0].startswith('+++'):
      return

    match = re.match(r'^\+\+\+ ([^\t]+).*$', line)
    if match:
      if not last_line.startswith('---'):
      if (self.mangle(match.group(1)) != self.filename and
          match.group(1) != '/dev/null'):
        # TODO(maruel): Can +++ be /dev/null? If so, assert self.is_delete ==
        # True.
      if lines:
        self._fail('Crap after +++')
      # We're done.
      return