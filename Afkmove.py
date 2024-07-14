import discord
from discord.ext import tasks

class Afkmove:
    def __init__(self, bot, guild_id, target_channel_id, voice_channel_ids):
        self.bot = bot
        self.guild_id = guild_id
        self.target_channel_id = target_channel_id
        self.voice_channel_ids = voice_channel_ids
        self.muted_users = {}

    def register_events(self):
        @self.bot.event
        async def on_voice_state_update(member, before, after):
            if after.mute and not before.mute:
                print(f'{member} was muted.')
                self.muted_users[member.id] = discord.utils.utcnow()
            elif not after.mute and before.mute:
                if member.id in self.muted_users:
                    print(f'{member} was unmuted.')
                    del self.muted_users[member.id]

    @tasks.loop(seconds=10)
    async def check_muted_users(self):
        guild = self.bot.get_guild(self.guild_id)
        if guild is None:
            print(f'Guild with ID {self.guild_id} not found.')
            return

        for voice_channel_id in self.voice_channel_ids:
            channel = guild.get_channel(voice_channel_id)
            if channel:
                for member in channel.members:
                    if member.voice and member.voice.self_mute:
                        member_id = member.id
                        if member_id in self.muted_users:
                            mute_time = self.muted_users[member_id]
                            if (discord.utils.utcnow() - mute_time).total_seconds() > 60:
                                print(f'{member} has been self-muted for more than 60 seconds.')
                                await member.move_to(guild.get_channel(self.target_channel_id))
                                print(f'Moved {member} to {self.target_channel_id}')
                                del self.muted_users[member_id]
                        else:
                            self.muted_users[member_id] = discord.utils.utcnow()

    async def start(self):
        self.check_muted_users.start()
