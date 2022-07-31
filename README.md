# impostor

Find Tor relays imitating your own relays.

Invalid relays must:

- Not be linked to a given `MyFamily` fingerprint.
- Use a given `ContactInfo` or `Nickname`.
- Be running.

## Usage

Install the dependencies into a Python virtual environment via `Pipfile` or
`requirements.txt`, then run `./impostor.py --help` for usage information.

Example:

```bash
./impostor.py A14D96E6C4C3A5AF3D7E57AC0A85AE82BDFB0F4B --contact artikel10 --nickname artikel10
```

Impostor generates no output if only valid relays are found, so you can run it
in a daily cronjob and receive emails only if invalid relays appear. The script
also returns an exit status of `1` in this case.
