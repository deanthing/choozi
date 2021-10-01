export interface IUserOut {
  name: string;
  group_id?: number;
  is_owner?: boolean;
  id?: string;
  token?: string;
}

export interface IUserIn {
  name: string;
  group_id: number;
  is_owner: boolean;
  id: number;
  token?: string;
}

interface IStreamingProviderOut {
  name: string;
}
interface IGenreOut {
  name: string;
}
interface IReleasePeriodOut {
  lower_bound: number;
  upper_bound: number;
}

interface IStreamingProviderIn {
  display_priority: number;
  logo_url: string;
  tmdb_id: number;
  name: string;
}
interface IGenreIn {
  name: string;
  tmdb_id: number;
  id: number;
}
interface IReleasePeriodIn {
  lower_bound: number;
  upper_bound: number;
  id: number;
}

export interface IGroupOut {
  genres: IGenreOut[];
  streaming_provider: IStreamingProviderOut[];
  release_period: IReleasePeriodOut[];
}

export interface IMovie {
  id: number;
  tmdb_id: number;
  title: string;
  blurb: string;
  picture_url: string;
  release_date: string;
  streaming_providers: IStreamingProviderIn[];
  genres: IGenreIn[];
}

interface ILike {
  group_id: number;
  movie_id: number;
  id: number;
}

export interface IGroupIn {
  id: number;
  in_waiting_room: boolean;
  room_code: string;
  users: IUserIn[];
  release_period: IReleasePeriodIn[];
  likes: ILike[];
  genres: IGenreIn[];
  movies: IMovie[];
}
