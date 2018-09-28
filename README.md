**Known Issues:**
- Creating monitors with `no_data_timeframe` left blank fails. However,
  modifying a monitor succeeds. I'm choosing to leave it like this, because
  the main use case for this script is to manage already existing monitors, and
  because I think it's more important that the option is visible to the user.
